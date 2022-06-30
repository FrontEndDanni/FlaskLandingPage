from flask import Blueprint, request, jsonify
from coffee_inventory.helpers import token_required 
from coffee_inventory.models import db, User, Coffee, coffee_schema, coffees_schema 


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some':'value'}

#CREATE COFFEE ENDPOINT
@api.route('/coffees', methods = ['POST'])
@token_required
def create_coffee(current_user_token):
    name = request.json['name']
    description = request.json['description']
    caffeine_level = request.json['caffeine_level']
    price = request.json['price']
    roast = request.json['roast'] 
    cost_of_production = request.json['cost_of_production']
    place_of_origin = request.json['place_of_origin']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token.token}")

    coffee = Coffee(name, description, caffeine_level, price, roast, cost_of_production, place_of_origin, user_token = user_token )

    db.session.add(coffee)
    db.session.commit()

    response = coffee_schema.dump(coffee)

    return jsonify(response)

#Retrieve ALL Coffee Endpoints

@api.route('/coffees', methods = ['GET'])
@token_required
def get_coffees(current_user_token):
    owner = current_user_token.token
    coffees = Coffee.query.filter_by(user_token = owner).all()
    response = coffees_schema.dump(coffees)
    return jsonify(response)

#Retrieve ONE Coffee Endpoint
@api.route('/coffees/<id>', methods = ['GET'])
@token_required
def get_coffee(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        coffee = Coffee.query.get(id)
        response = coffee_schema.dump(coffee)
        return jsonify(response)
    else: 
        return jsonify({'message': 'Valid Token Required'}), 401

#Update Coffee
@api.route('/coffees/<id>', methods = ['POST', 'PUT'])
@token_required
def update_coffee(current_user_token, id):
    coffee = Coffee.query.get(id)

    coffee.name = request.json['name']
    coffee.description = request.json['description']
    coffee.caffeine_level = request.json['caffeine_level']
    coffee.price = request.json['price']
    coffee.roast = request.json['roast'] 
    coffee.cost_of_production = request.json['cost_of_production']
    coffee.place_of_origin = request.json['place_of_origin']
    coffee.user_token = current_user_token.token

    db.session.commit()
    response = coffee_schema.dump(coffee)
    return jsonify(response)

#Delete Coffee Endpoint
@api.route('/coffees/<id>', methods=['DELETE'])
@token_required
def delete_coffee(current_user_token, id):
    coffee = Coffee.query.get(id)
    db.session.delete(coffee)
    db.session.commit()
    response = coffee_schema.dump(coffee)
    return jsonify(response)