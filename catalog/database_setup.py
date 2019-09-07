"""
Database setup for the Item Catalog project.

This script should be run first before running the main application.py.
however, application.py will run this script automatically if no database found in current project.

"""

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Get the base class mapper from SQLalchemy
Base = declarative_base()

# Create user table to store user information


class User(Base):
    """Setup a database table of registered users.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the user ID.
        name: A column for the name of the user.
        email: A column for the user's email.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

# Create catagory table to store different categories of Item Catalog


class Category(Base):
    """Define a database table of categories that an item will belong to.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the category ID.
        name: A column for the name of the category.
        items: A relationship with Item so a category knows about the items
            it contains.
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    items = relationship('Item', cascade="save-update, merge, delete")

    @property
    def serialise(self):
        # Returns category data in an easily serialiseable format.
        return {
            'id': self.id,
            'name': self.name,
            'Item': [i.serialise for i in self.items]
        }

# Create Item table to store item information


class Item(Base):
    """Define a database table of items.

    Attributes:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the item ID.
        name: A column to store the name of the item.
        description: A column to store a description of the item.
        quantity: Number of items.
        category_id: A column to store the ID of the category that the item
            belongs to.
        category: Makes a one-to-one relationship to the Category class.
        user_id: A column to store the user ID of the owner of an item.
        user: Make a one-to-one relationship to the User class.
    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialise(self):
        """Returns item data in an easily serialiseable format."""
        return {
            'id': self.id,
            'cat_id': self.category_id,
            'name': self.name,
            'description': self.description
        }


def create_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print "Database created successfully!"
