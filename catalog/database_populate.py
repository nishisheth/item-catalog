"""
This script add some items to the item catalog database. 

"""
from sqlalchemy import func
from database_setup import User, Category, Item
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
    user1 = User(name="John Smith", email="john.smith@easygrocery.com")
    session.add(user1)
    session.commit()

    # Adding some items to Fruits&Veg category
    fvitem1 = Item(
        user=user1,
        category=category1,
        name="Apple Royal Gala",
        description=(
            "Round shaped fruit medium in size with red skin and a cream coloured flesh with a sweet flavour."
        )
    )
    session.add(fvitem1)
    session.commit()

    fvitem2 = Item(
        user=user1,
        category=category1,
        name="Green Seedless Grapes",
        description=(
            "Medium-sized, oval shaped grapes with light green skin and pale green flesh, seedless."
        )
    )
    session.add(fvitem2)
    session.commit()

    fvitem3 = Item(
        user=user1,
        category=category1,
        name="Broccolini",
        description=(
            "Natural cross between broccoli and Chinese broccoli (gaai lan). It has a long slender stem topped with small flowering buds that are a cross between broccoli florets and an asparagus tip."
        )
    )
    session.add(fvitem3)
    session.commit()

    fvitem4 = Item(
        user=user1,
        category=category1,
        name="Red Capsicum",
        description=(
            "Capsicums are seed pods. A shiny red vegetable with crisp, moist flesh. Hollow with a seeded core. Capsicums are sweet and juicy with a mild spicy flavour. Red capsicums, being riper, are sweeter than green capsicums."
        )
    )
    session.add(fvitem4)
    session.commit()

    fvitem5 = Item(
        user=user1,
        category=category1,
        name="Red Capsicum",
        description=(
            "White Potato best For mashing is soft and fluffy contains Vitamin C, which helps support your immune system, healthy brain function and can reduce tiredness."
        )
    )
    session.add(fvitem5)
    session.commit()

    # Adding some items to Meat&Seafood category
    msitem1 = Item(
        user=user1,
        category=category2,
        name="Roast Butterflied Chicken",
        description=(
            "Roast Butterflied Chicken packed in 1kg bag."
        )
    )
    session.add(msitem1)
    session.commit()

    msitem2 = Item(
        user=user1,
        category=category2,
        name="Slow Cooked Beef Chuck Steak",
        description=(
            " Slow Cooked Beef Chuck Steak in 500g bag."
        )
    )
    session.add(msitem2)
    session.commit()

    # Adding some items to Bakery category
    bitem1 = Item(
        user=user1,
        category=category3,
        name="Lemon Tart Large",
        description=(
            "Lemon Tart Large 500g"
        )
    )
    session.add(bitem1)
    session.commit()

    bitem2 = Item(
        user=user1,
        category=category3,
        name="Chocolate cookies",
        description=(
            "Chocolate cookies pack of 12"
        )
    )
    session.add(bitem2)
    session.commit()

    # Adding some items to Dairy category
    ditem1 = Item(
        user=user1,
        category=category4,
        name="Full Cream Milk",
        description=(
            "Full Cream Milk offers a better deal for farmers and helps to support them and their families."
        )
    )
    session.add(ditem1)
    session.commit()

    ditem2 = Item(
        user=user1,
        category=category4,
        name="Skim Cream Milk",
        description=(
            "Skim Cream Milk has less fat than full cream milk."
        )
    )
    session.add(ditem2)
    session.commit()

    session.close()
    print "Added some items in database successfully!"

if __name__ == '__main__':
    database_populate()
