"""
This script add some items to the item catalog database.

"""
from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, Item, Base
from connect_database import connect_database


def database_populate():
    """Populate the item catalog database some initial content."""
    session = connect_database()

    # Make sure the database is empty before running this inital data dump.
    category_count = session.query(func.count(Category.id)).scalar()
    if category_count > 0:
        session.close()
        return

    # Create the six categories items fall in to.
    category1 = Category(name="Fruits & Veg")
    session.add(category1)
    session.commit()

    category2 = Category(name="Meat & Seafood")
    session.add(category2)
    session.commit()

    category3 = Category(name="Bakery")
    session.add(category3)
    session.commit()

    category4 = Category(name="Dairy")
    session.add(category4)
    session.commit()

    # Create a dummy user to populate initial items
    user1 = User(name="John Smith",
                 email="john.smith@easygrocery.com")
    session.add(user1)
    session.commit()

    # Adding some items to Fruits&Veg category
    fvitem1 = Item(
        user=user1,
        category=category1,
        name="Apple Royal Gala",
        description="Round shaped fruit medium in size with red skin.")
    session.add(fvitem1)
    session.commit()

    fvitem2 = Item(
        user=user1,
        category=category1,
        name="Green Seedless Grapes",
        description="Medium-sized, oval shaped grapes.")
    session.add(fvitem2)
    session.commit()

    # # Adding some items to Meat&Seafood category

    msitem1 = Item(
        user=user1,
        category=category2,
        name="Chicken",
        description="Roast Butterflied Chicken packed in 1kg bag.")
    session.add(msitem1)
    session.commit()

    msitem2 = Item(
        user=user1,
        category=category2,
        name="Tuna fish",
        description="Packed tuna fish")
    session.add(msitem2)
    session.commit()

    # Adding some items to Bakery category
    bitem1 = Item(
        user=user1,
        category=category3,
        name="Cup Cakes",
        description="Cup cakes special 12 packs")
    session.add(bitem1)
    session.commit()

    bitem2 = Item(
        user=user1,
        category=category3,
        name="Lemon Tart Large",
        description="Lemon Tart Large 500g")
    session.add(bitem2)
    session.commit()

    bitem3 = Item(
        user=user1,
        category=category3,
        name="Chocolate cookies",
        description="Chocolate cookies pack of 12")
    session.add(bitem3)
    session.commit()

    # Adding some items to Dairy category
    ditem1 = Item(
        user=user1,
        category=category4,
        name="Full Cream Milk",
        description="Full Cream Milk 3L")
    session.add(ditem1)
    session.commit()
    ditem2 = Item(
        user=user1,
        category=category4,
        name="Skim Cream Milk",
        description="Skim Cream Milk 3L")
    session.add(ditem2)
    session.commit()

    session.close()

    print "Added some items in database successfully!"


if __name__ == '__main__':
    database_populate()
