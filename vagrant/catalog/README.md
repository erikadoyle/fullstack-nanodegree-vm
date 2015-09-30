This project contains the code to run a web application that displays a catalog of items. It also contains the code to
setup and populate the app's database backend. This code intended for educational purposes only in fulfillment of the "Project 3: Item Catalog" for the Udacity Full Stack Web Developer Nanodegree program.

# Prerequisites
 - VirtualBox installation (https://www.virtualbox.org/wiki/Downloads)
 - Vagrant installation (https://www.vagrantup.com/downloads)
 - Clone of this respository (git clone http://github.com/erikadoyle/fullstack-nanodegree-vm fullstack)

To run the web application locally:

From a GitHub shell:
 1. cd fullstack/vagrant
 2. vagrant up (you can turn off the VM with 'vagrant halt')
 3. vagrant ssh (from here you can type 'exit' to log out)
 4. sudo pip install werkzeug==0.8.3
 5. sudo pip install flask==0.9
 6. sudo pip install Flask-Login==0.1.3
 7. cd /vagrant/catalog
 8. python database_setup.py
 9. python populate_plantnurserydb.py
 10. python application.py
 11. Navigate to http://localhost:8000

# Credits
All images are copyright Greg Rabourn and used with his permission. Plant species data is from the
 [King County Native Plant Guide](https://green2.kingcounty.gov/gonative/) of Washington State.
The OAuth code used in this project is based off of class examples from the Udacity
[Authentication and Authorization](https://www.udacity.com/course/authentication-authorization-oauth--ud330) course.
The basic structure of the Flask application and SQLAlchemy code is based off of coursework from the Udacity
[Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088), but modified, extended and
refactored for the specific purposes of this catalog application.
