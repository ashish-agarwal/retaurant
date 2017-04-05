import os
from flask import render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask import session as login_session
# from werkzeug import secure_filename
from sqlalchemy import desc, literal, and_
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from db.database_setup import Restaurant, MenuItem, User
from db.db_helper import connect_to_database


@app.route('/')
def show_homepage():
    """Show the homepage displaying the categories and latest items.

    Returns:
        A web page with the 10 latest items that have added.
    """
    session = connect_to_database(app)

    restaurants = session.query(Restaurant).all()

    session.close()
    if not restaurants:
        flash("There are currently no items in this category.")

    return render_template("restaurants.html", restaurants=restaurants)


@app.route('/restaurant', methods=['POST'])
def add_restaurant():
    if 'username' not in login_session:
        return redirect('/')

    session = connect_to_database(app)
    if request.method == 'POST':
        # Restaurant names for a restaurant must be unique
        qry = session.query(Restaurant).filter(Restaurant.name == request.form[
            'name'])
        already_exists = (session.query(literal(True)).
                          filter(qry.exists()).scalar())
        if already_exists is True:
            flash("Error: There is already a restaurant with the name '%s'"
                  % request.form['name'])
            session.close()
            return redirect('/')

        new_item = Restaurant(name=request.form['name'])
        session.add(new_item)
        session.commit()
        flash("New restaurant successfully created!")
        session.close()

        return redirect('/')


@app.route('/restaurant/<restaurant_id>/items/')
def show_items(restaurant_id):
    session = connect_to_database(app)

    try:
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        flash("The restaurant '%s' does not exist." % restaurant_id)
        return redirect(url_for('show_homepage'))

    items = (session.query(MenuItem).filter_by(restaurant=restaurant).
             order_by(MenuItem.name).all())
    session.close()
    if not items:
        flash("There are currently no items in this restaurant.")
    return render_template("items.html", restaurant=restaurant, items=items)


@app.route('/restaurant/<restaurant_id>/item/', methods=['GET', 'POST'])
def add_item(restaurant_id):
    if 'username' not in login_session:
        return redirect('/')

    session = connect_to_database(app)
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        session.close()
        return render_template('newitem.html',
                               restaurants=restaurants)

    if request.method == 'POST':
        try:
            restaurant = session.query(
                Restaurant).filter_by(id=restaurant_id).one()
        except NoResultFound:
            flash("The restaurant does not exist.")
            return redirect(url_for('show_homepage'))

        # Item names for a restaurant must be unique
        qry = session.query(MenuItem).filter(and_(MenuItem.name == request.form[
            'name'], MenuItem.restaurant_id == restaurant_id))
        already_exists = (session.query(literal(True)).
                          filter(qry.exists()).scalar())
        if already_exists is True:
            flash("Error: There is already an animal with the name '%s'"
                  % request.form['name'])
            session.close()
            return redirect(url_for('show_items', restaurant_id=restaurant_id))

        new_item = MenuItem(restaurant=restaurant,
                            name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            course=request.form['course'],
                            user_id=login_session['user_id'])
        session.add(new_item)
        session.commit()
        flash("New item successfully created!")
        items = (session.query(MenuItem).filter_by(restaurant=restaurant).
                 order_by(MenuItem.name).all())
        session.close()

        return redirect(url_for('show_items', restaurant_id=restaurant_id))


@app.route('/restaurant/<restaurant_id>/item/<item_id>', methods=['GET'])
def show_item(restaurant_id, item_id):
    session = connect_to_database(app)
    restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        session.close()
        flash("The item '%s' does not exist." % item_id)
        return redirect(url_for('show_homepage'))

    session.close()    
    return render_template('item.html',
                               restaurant=restaurant, item=item)


@app.route('/restaurant/<restaurant_id>/item/<item_id>/delete', methods=['GET'])
def delete_item(restaurant_id, item_id):
    """Delete a specified item from the database.
    """
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_to_database(app)

    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_id)
        session.close()
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't create this ite,, so you can't delete it.")
        session.close()
        return redirect(url_for('show_items', restaurant_id=restaurant_id))

    session.delete(item)
    session.commit()

    flash("Item successfully deleted!")
    session.close()
    return redirect(url_for('show_items', restaurant_id=restaurant_id))


@app.route('/restaurant/<restaurant_id>/item/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(restaurant_id, item_id):
    """Edit item from the database.
    """
    if 'username' not in login_session:
        return redirect('/login')

    session = connect_to_database(app)

    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_id)
        session.close()
        return redirect(url_for('show_homepage'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't create this item, so you can't edit it.")
        session.close()
        return redirect(url_for('show_items', restaurant_id=restaurant_id))

    if request.method == 'GET':
        return render_template('edit_item.html', restaurant_id=restaurant_id,
                               item=item)

    if request.method == 'POST':
        # Item names for a restaurant must be unique
        if request.form['name'] != item.name:
            qry = session.query(MenuItem).filter(and_(MenuItem.name == request.form[
                'name'], MenuItem.restaurant_id == restaurant_id))
            already_exists = (session.query(literal(True)).
                              filter(qry.exists()).scalar())
            if already_exists is True:
                flash("Error: There is already an animal with the name '%s'"
                      % request.form['name'])
                session.close()
                return redirect(url_for('show_items', restaurant_id=restaurant_id))
            item.name = request.form['name']

        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']

        session.add(item)
        session.commit()

        flash("Item successfully edited!")
        session.close()
        return redirect(url_for('show_items', restaurant_id=restaurant_id))
