"""Defines JSON API endpoints."""
from flask import jsonify, redirect, url_for, flash
from sqlalchemy.orm.exc import NoResultFound

from catalog import app
from db.database_setup import Restaurant, MenuItem, User
from db.db_helper import connect_to_database


@app.route('/restaurants/json/')
def restaurants():
    session = connect_to_database(app)
    restaurants = session.query(Restaurant).all()
    serialised_restaurants = [i.serialize for i in restaurants]
    session.close()
    return jsonify(restaurants=serialised_restaurants)


@app.route('/restaurants/<restaurant_id>/items/json/')
def items_json(restaurant_id):
    session = connect_to_database(app)
    try:
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
    except NoResultFound:
        return "The restaurant '%s' does not exist." % restaurant_id

    items = (session.query(MenuItem).filter_by(restaurant=restaurant).
             order_by(MenuItem.name).all())
    serialised_restaurants = [i.serialize for i in items]
    session.close()
    return jsonify(items=serialised_restaurants)


@app.route('/restaurants/<restaurant_id>/items/<item_id>/json/')
@app.route('/item/<item_id>/json/')
def item_json(restaurant_id, item_id):
    session = connect_to_database(app)
    try:
        item = session.query(MenuItem).filter_by(id=item_id).one()
    except NoResultFound:
        session.close()
        flash("JSON error: The item '%s' does not exist." % item_name)
        return redirect(url_for('show_homepage'))

    session.close()
    return jsonify(Item=item.serialize)
