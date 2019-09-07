#!/usr/bin/env python
"""
Main Python script that starts the item catalog app.

It checks to see if the database file exists and if not it creates the database
and populates it with some sample content. 

"""
import os.path

from database_setup import create_db
from database_populate import database_populate
from connect_database import connect_database
from flask import Flask
from flask import session as login_session
from flask_seasurf import SeaSurf
from database_setup import Category, Item, User
from sqlalchemy import desc, literal
from flask import request, render_template, redirect, url_for, flash, jsonify
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy.orm.exc import NoResultFound
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
csrf = SeaSurf(app)

# Login - Show the login screen to the user.
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    session = connect_database()
    categories = session.query(Category).all()
    session.close()

    return render_template('login.html', STATE=state, categories=categories)

# Google Auth endpoint 
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Performs app login via Google oauth."""
    client_secrets_file = ('client_secrets.json')
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization one-time code into a credentials object
        oauth_flow = flow_from_clientsecrets(client_secrets_file, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    g_client_id = json.loads(
        open(client_secrets_file, 'r').read())['web']['client_id']
    if result['issued_to'] != g_client_id:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['email'] = data["email"]

    # Check if the user exists in the database. If not create a new user.
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        user_id = create_user()
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("You are now logged in as %s" % login_session['username'])
    print "User has successfully logged into app!"
    return output

# Google Auth disconnet 
def gdisconnect():
    """Revoke a current user's token and reset their login session."""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# Logout - Removes google auth tokens from session 
@app.route('/logout')
def logout():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.")
        return redirect(url_for('show_homepage'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('show_homepage'))

# Creates a new user in the database 
def create_user():
    new_user = User(name=login_session['username'],
                    email=login_session['email'])
    session = connect_database()
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.close()
    return user.id

# Retruns userId from email address
def get_user_id(email):
    session = connect_database()
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user.id
    except NoResultFound:
        session.close()
        return None

# Home page or default page shows the item categories and 5 latest items 
@app.route('/')
@app.route('/catalog/')
def show_homepage():
    session = connect_database()
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(desc(Item.id))[0:6]
    session.close()
    return render_template('index.html',
                           categories=categories,
                           latest_items=latest_items)

# Gets items beloging to specifice category
@app.route('/catalog/<category_name>/items/')
def show_items(category_name):
    session = connect_database()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        return redirect(url_for('show_homepage'))

    categories = session.query(Category).all()
    items = (session.query(Item).filter_by(category=category).
             order_by(Item.name).all())
    session.close()
    if not items:
        flash("There are no items in this category.")
    return render_template('items.html',
                           categories=categories,
                           category=category,
                           items=items)

# Shows items added by user
@app.route('/catalog/myitems/')
def show_my_items():
    if 'username' not in login_session:
        return redirect('/login')

    user_id = get_user_id(login_session['email'])
    session = connect_database()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(user_id=user_id).all()
    session.close()

    if not items:
        flash("You haven't add any items yet.")
        redirect(url_for('show_homepage'))

    return render_template('user_items.html',
                           categories=categories,
                           items=items)

@app.route('/catalog/<category_name>/<item_name>/')
def show_item(category_name, item_name):
    """Show details of a particular item belonging to a specified category.

    Args:
        category_name (str): The name of the category to which the item
            belongs.
        item_name (str): The name of the item.

    Returns:
        A web page showing information of the requested item.
    """
    session = connect_database()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        session.close()
        return redirect(url_for('show_homepage'))

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('show_items', category_name=category_name))

    user = session.query(User).filter_by(id=item.user_id).one()
    ower_name = user.name

    categories = session.query(Category).all()
    session.close()
    return render_template('item.html',
                           categories=categories,
                           category=category,
                           item=item,
                           ower_name=ower_name)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def create_item():
    """Allow users to create a new item in the catalog."""
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_database()

    if request.method == 'POST':
        if not request.form['name']:
            flash("New item not created: No name provided.")
            return redirect(url_for('show_homepage'))

        if request.form['name'] == "items":
            # Can't have an item called "items" as this is a route.
            flash("Error: Can't have an item called 'items'.")
            return redirect(url_for('show_homepage'))

        # Enforce rule that item names are unique
        qry = session.query(Item).filter(Item.name == request.form['name'])
        already_exists = (session.query(literal(True)).
                          filter(qry.exists()).scalar())
        if already_exists is True:
            flash("Error: There is already an item with the name '%s'"
                  % request.form['name'])
            session.close()
            return redirect(url_for('show_homepage'))

        category = (session.query(Category)
                    .filter_by(name=request.form['category']).one())
        new_item = Item(category=category,
                        name=request.form['name'],
                        description=request.form['description'],
                        user_id=login_session['user_id'])

        session.add(new_item)
        session.commit()

        flash("New item successfully created!")
        category_name = category.name
        item_name = new_item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()

        # See, if any, which category page new item was click on.
        ref_category = None
        if request.referrer and 'catalog' in request.referrer:
            ref_url_elements = request.referrer.split('/')
            if len(ref_url_elements) > 5:
                ref_category = ref_url_elements[4]

        session.close()
        return render_template('new_item.html',
                               categories=categories,
                               ref_category=ref_category)


@app.route('/catalog/<category_name>/<item_name>/edit/',
           methods=['GET', 'POST'])
@app.route('/catalog/<item_name>/edit/', methods=['GET', 'POST'])
def edit_item(item_name, category_name=None):
    """Edit the details of the specified item.

    Args:
        item_name (str): Name of item to be edited.
        category_name (str): Optionally, can also specify the category to
            which the item belongs to.
    """
    if 'username' not in login_session:
        flash("Please login inorder to edit an item.")
        return redirect('/login')

    session = connect_database()

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You cannot delete other user's items.")
        category = session.query(Category).filter_by(id=item.category_id).one()
        category_name = category.name
        item_name = item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))

    if request.method == 'POST':
        if request.form['name'] != item.name:
            # Enforce rule that item names are unique
            qry = session.query(Item).filter(Item.name == request.form['name'])
            already_exists = (session.query(literal(True)).filter(qry.exists())
                              .scalar())
            if already_exists is True:
                original_category = (session.query(Category)
                                     .filter_by(id=item.category_id).one())
                flash("Error: There is already an item with the name '%s'"
                      % request.form['name'])
                session.close()
                return redirect(url_for('show_items',
                                        category_name=original_category.name))
            item.name = request.form['name']

        form_category = (session.query(Category)
                         .filter_by(name=request.form['category']).one())
        if form_category != item.category:
            item.category = form_category

        item.description = request.form['description']
        session.add(item)
        session.commit()

        flash("Item successfully edited!")
        category_name = form_category.name
        item_name = item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


@app.route('/catalog/<item_name>/delete/', methods=['GET', 'POST'])
def delete_item(item_name):
    """Delete a specified item from the database.

    Args:
        item_name (str): Name of the item to be deleted.
    """
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_database()

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't add this item, so you can't delete it. Sorry :-(")
        category = session.query(Category).filter_by(id=item.category_id).one()
        category_name = category.name
        item_name = item.name
        session.close()
        return redirect(url_for('show_item',
                                category_name=category_name,
                                item_name=item_name))

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        category = session.query(Category).filter_by(id=item.category_id).one()

        flash("Item successfully deleted!")
        category_name = category.name
        session.close()
        return redirect(url_for('show_items', category_name=category_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('delete_item.html',
                               categories=categories,
                               item=item)

#JSON endpoints for item catalog 
@app.route('/catalog/JSON/')
@app.route('/catalog.json/')
def catalog_json():
    """Returns all the items in the catalog as a JSON file.

    The for loop in the call to jsonify() goes through each category and,
    because the Category class has a reference to the items in it, for each
    item a call to its serialise function is made. So we end up with a JSON
    array of items for each category.
    """
    session = connect_database()
    categories = session.query(Category).all()
    serialised_catergories = [i.serialise for i in categories]
    session.close()
    return jsonify(Category=serialised_catergories)

@app.route('/catalog/<category_name>/<item_name>/JSON/')
@app.route('/catalog/<item_name>/JSON/')
def item_json(item_name, category_name=None):
    """Returns a single item in a JSON file.

    Args:
        item_name (str): The name of the item to return in JSON format.
        category_name (str): A dummy variable used so that the path can
            optionally include the category name.
    """
    session = connect_database()
    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        session.close()
        flash("JSON error: The item '%s' does not exist." % item_name)
        return redirect(url_for('show_homepage'))

    session.close()
    return jsonify(Item=item.serialise)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    
    if os.path.isfile('itemcatalog.db') is False:
            create_db('sqlite:///itemcatalog.db')
            database_populate()

    app.debug = True
    app.run(host='0.0.0.0', port=8000)
