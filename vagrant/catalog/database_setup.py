from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# Construct a base class for the following class definitions
Base = declarative_base()


class User(Base):
    """Represents an authenticated user (department curator) of the site"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    """Represents a type of plant nursery species

    These are all common names for broad plant categories, such as trees,
    shrubs, groundcover, grasses and vines

    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(String(255))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Species(Base):
    """Represents a specific nursery plant species"""
    __tablename__ = 'species'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    scientific_name = Column(String(100))
    moisture_reqs = Column((String(50)))
    exposure_reqs = Column((String(50)))
    description = Column(String(250))
    image = Column(String(255))
    caption = Column(String(30))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'scientific_name': self.scientific_name,
            'moisture_reqs': self.moisture_reqs,
            'exposure_reqs': self.exposure_reqs,
            'description': self.description,
            'id': self.id
        }

engine = create_engine('sqlite:///plantnursery.db')

Base.metadata.create_all(engine)
