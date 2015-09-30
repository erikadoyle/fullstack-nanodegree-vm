# Imports for basic web app
import os.path
from flask import Flask, render_template, request, redirect, jsonify, \
url_for, flash, send_from_directory
from werkzeug import secure_filename

# Imports for database and server functionality
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Species, User

# Imports for OAuth functionality
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

UPLOAD_FOLDER = os.path.realpath('.') + '/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Create a database dngine and connect it to the db
engine = create_engine('sqlite:///plantnursery.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def show_login():
    """Routes the user to the sign-in page

    Returns (serves) the login page to the user
    """
    # Create an anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Authenticates the user via Google+ OAuth

    Returns the HTTP response for the attempted login
    """
    # Validate the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    # Attempt to upgrade the authorization code into a credentials object
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Ensure the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                 'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # Populate the login_session object
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Add Google as the OAuth login provider for the session
    login_session['provider'] = 'google'

    # If the user doesn't already exist, create a new database entry
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += login_session['username']
    flash("You are now logged in as: %s" % login_session['username'])
    return output


def createUser(login_session):
    """Helper function to create a new user entry in the database

    Args:
        login_session: Dictionary with the login session data

    Returns the new user ID string
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Helper function to lookup info on a specific user in the database

    For more info see the 'User' class in database_setup.py

    Args:
        user_id: ID string of the user to lookup

    Returns an object representing the requested user
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Helper function to get the user ID given a user login (email) name

    Args:
        email: User login (email) name

    Returns the Id string for the requested user
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects a user signed in with Google+ OAuth

    Returns the HTTP response for the attempted disconnect
    """
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke the current user's token and reset their login session
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # Report if the given token was invalid
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/department/<int:category_id>/species/JSON')
def categorySpecies_to_JSON(category_id):
    """Serializes all the species of a given department in JSON format

    Args:
        category_id: The ID of the department for the serialized species info

    Returns a JSON string with all the species info for the requested department
    """
    category = session.query(Category).filter_by(id=category_id).one()
    species = session.query(Species).filter_by(
        category_id=category_id).all()
    return jsonify(species=[i.serialize for i in species])


@app.route('/department/<int:category_id>/species/<int:species_id>/JSON')
def species_to_JSON(category_id, species_id):
    """Serializes the info for a specific species in JSON format

    Args:
        category_id: The ID of the department for the species
        species_id:  The ID of the species for serialized info

    Returns a JSON string for the species info of the requested department
    """
    species = session.query(Species).filter_by(id=species_id).one()
    return jsonify(species=species.serialize)


@app.route('/department/JSON')
def categories_to_JSON():
    """Serializes all the departments in the database to JSON format

    Returns a JSON string with all the department names
    """
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/')
@app.route('/department/')
def show_categories():
    """Displays all the departments of the PNW Native Plant Collection db

    Returns (serves) the department info page to the user / curator
    """
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publicCategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)


# Create a new category
@app.route('/department/new/', methods=['GET', 'POST'])
def new_category():
    """Displays the 'New department' edit page

    Returns (serves) the 'New department' page to the user (or the departments
    list if a new department entry was just submitted from the form)
    """
    # Check if the user is authenticated to the site
    if 'username' not in login_session:
        return redirect('/login')

    # Handle POST and GET requests
    if request.method == 'POST':
        # Based on image upload technique described at
        # http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
        image=request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        newCategory = Category(
            name=request.form['name'],
            user_id=login_session['user_id'],
            image=filename)
        session.add(newCategory)
        flash('New department created: %s' % newCategory.name)
        session.commit()
        return redirect(url_for('show_categories'))
    else:
        return render_template('newCategory.html')


@app.route('/department/<int:category_id>/edit/', methods=['GET', 'POST'])
def edit_category(category_id):
    """Displays the edit page for a specific department

    Args:
        category_id: The ID of the department to edit

    Returns (serves) the edit page for the requested department to the user
    (or the departments list if an edit was just submitted)
    """
    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session:
        return redirect('/login')

    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        authError = "<body>"
        authError = "   <p>You are not authorized to edit this department."
        authError += "  Please create your own department in order to edit."
        authError += "  <script>"
        authError += "      setTimeout(function() {"
        authError += "          window.location.href = '/category';"
        authError += "      }, 2000);"
        authError += "  </script>"
        return authError

    # Handle POST and GET requests
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.files['image']:
            image=request.files['image']
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedCategory.image = filename
        flash('Edited category: %s' % editedCategory.name)
        return redirect(url_for('show_species', category_id=category_id))
    else:
        return render_template('editCategory.html', category=editedCategory)


@app.route('/department/<int:category_id>/delete/', methods=['GET', 'POST'])
def delete_category(category_id):
    """Displays the delete page for a specific department

    Args:
        category_id: The ID of the department to delete

    Returns (serves) the delete page for the requested department to the user
    (or the departments list if a deletion was just submitted)
    """
    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session:
        return redirect('/login')

    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        authError = "<body>"
        authError = "   <p>You are not authorized to delete this department."
        authError += "  Please create your own department in order to delete."
        authError += "  <script>"
        authError += "      setTimeout(function() {"
        authError += "          window.location.href = '/category';"
        authError += "      }, 2000);"
        authError += "  </script>"
        return authError

    # Handle POST and GET requests
    if request.method == 'POST':
        # Delete the image and category
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], categoryToDelete.image))
        session.delete(categoryToDelete)
        # Delete its associated species
        speciesToDelete = session.query(Species).filter_by(
                category_id=category_id).all()
        for species in speciesToDelete:
            # First delete the associated image
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], species.image))
            session.delete(species)
        flash('Deleted department: %s' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('show_categories', category_id=category_id))
    else:
        return render_template('deleteCategory.html',
                               category=categoryToDelete)


@app.route('/images/<filename>')
def uploaded_file(filename):
    """Serves the image files for the site

    Returns (serves) the HTTP requested image
    """
    # From sample code at http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/department/<int:category_id>/')
@app.route('/department/<int:category_id>/species/')
def show_species(category_id):
    """Displays all the species for a given department

    Args:
        category_id: The ID of the department for which to display species


    Returns (serves) the department's species info page to the user / curator
    """
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    species = session.query(Species).filter_by(
        category_id=category_id).all()

    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session \
            or creator.id != login_session['user_id']:
        return render_template('publicSpecies.html', species=species,
                               category=category)
    else:
        return render_template('species.html', species=species,
                               category=category)


def allowed_file(filename):
    """Checks a file name to determine if its file type is supported

    Args: name of the file (e.g., 'mypicture.jpg')

    Returns true if file type is allowed, false otherwise
    """
    # From sample code at http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route(
    '/department/<int:category_id>/species/new/', methods=['GET', 'POST'])
def new_species(category_id):
    """Displays the species add page for a specific department

    Args:
        category_id: The ID of the department for which to add a new species

    Returns (serves) the department's 'Add new species' page to the curator
    (or the department's species listing page if an addition was submitted)
    """
    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        authError = "<body>"
        authError = "   <p>You are not authorized to add a species to this "
        authError += "  department. Please create your own department."
        authError += "  <script>"
        authError += "      setTimeout(function() {"
        authError += "          window.location.href = '/category';"
        authError += "      }, 2000);"
        authError += "  </script>"
        return authError

    # Handle POST and GET requests
    if request.method == 'POST':
        # Based on image upload technique described at
        # http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
        image=request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        caption = request.form['caption'] if request.form['caption'] else ""
        newSpecies = Species(name=request.form['name'],
                             scientific_name=request.form['scientific_name'],
                             moisture_reqs=request.form['moisture_reqs'],
                             exposure_reqs=request.form['exposure_reqs'],
                             description=request.form['description'],
                             image=filename,
                             caption=caption,
                             category_id=category_id,
                             user_id=category.user_id)
        session.add(newSpecies)
        session.commit()
        flash('New species added: %s' % (newSpecies.name))
        return redirect(url_for('show_species', category_id=category_id))
    else:
        return render_template('newSpecies.html', category=category,
                               category_id=category_id)


@app.route('/department/<int:category_id>/species/<int:species_id>/edit',
           methods=['GET', 'POST'])
def edit_species(category_id, species_id):
    """Displays the edit page for a specific species

    Args:
        category_id: The ID of the department containing the species to edit
        species_id: The ID of the species for which to edit info

    Returns (serves) the edit page for the requested species to the curator
    """
    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session:
        return redirect('/login')

    editedItem = session.query(Species).filter_by(id=species_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        authError = "<body>"
        authError = "   <p>You are not authorized to edit the species in this "
        authError += "  department. Please create your own department."
        authError += "  <script>"
        authError += "      setTimeout(function() {"
        authError += "          window.location.href = '/category';"
        authError += "      }, 2000);"
        authError += "  </script>"
        return authError

    # Handle POST and GET requests
    if request.method == 'POST':
        # Based on image upload technique described at
        # http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
        if request.files['image']:
            image=request.files['image']
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                editedItem.image = filename
        if request.form['caption']:
            editedItem.caption = request.form['caption']
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['scientific_name']:
            editedItem.scientific_name = request.form['scientific_name']
        if request.form['moisture_reqs']:
            editedItem.moisture_reqs = request.form['moisture_reqs']
        if request.form['exposure_reqs']:
            editedItem.exposure_reqs = request.form['exposure_reqs']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.commit()
        flash('Edited species: %s' % editedItem.name)
        return redirect(url_for('show_species', category_id=category_id))
    else:
        return render_template(
            'editSpecies.html', category_id=category_id,
            species_id=species_id, species=editedItem, category=category)


@app.route('/department/<int:category_id>/species/<int:species_id>/delete',
           methods=['GET', 'POST'])
def delete_species(category_id, species_id):
    """Displays the delete page for a specific species

    Args:
        category_id: The ID of the department containing the species to delete
        species_id: The ID of the species to delete

    Returns (serves) the delete page for the requested species to the curator
    """
    # Check if the user is authenticated to the site and is this dept's curator
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Species).filter_by(id=species_id).one()
    if login_session['user_id'] != category.user_id:
        authError = "<body>"
        authError = "   <p>You are not authorized to edit the species in this "
        authError += "  department. Please create your own department."
        authError += "  <script>"
        authError += "      setTimeout(function() {"
        authError += "          window.location.href = '/category';"
        authError += "      }, 2000);"
        authError += "  </script>"
        return authError

    # Handle POST and GET requests
    if request.method == 'POST':
        # Delete the image
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], itemToDelete.image))

        # Delete the database entry
        session.delete(itemToDelete)
        session.commit()
        flash('Deleted species: %s' % itemToDelete.name)
        return redirect(url_for('show_species', category_id=category_id))
    else:
        return render_template('deleteSpecies.html', species=itemToDelete,
                               category=category, category_id=category_id)


@app.route('/disconnect')
def disconnect():
    """Logs out the current user

    Currently only Google+ is supported as an OAuth provider

    Returns (serves) the public page of PNW Plant Collection departments
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You are now logged out.")
        return redirect(url_for('show_categories'))
    else:
        flash("You were not logged in")
        return redirect(url_for('show_categories'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
