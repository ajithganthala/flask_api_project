# -*- coding: utf-8 -*-
"""
Created on 16-06-2023
@author: ajith.ganthala
"""

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.exc import SQLAlchemyError

api_object = Flask(__name__)
sql_pass = 'password'
api_object.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://username:{sql_pass}@localhost/dbname'
api_object.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
sq_database = SQLAlchemy(api_object)

# Function to Create Toy Table MOdel
class Toy(sq_database.Model):
    """
    This class will create a table in Data base with mentioned name and schema
    """
    __tablename__ = 'toys_data'  #Can mention the tabke name here
    unique_id = sq_database.Column(sq_database.Integer, primary_key=True, autoincrement=True) ##will generate a unique number in the table
    name = sq_database.Column(sq_database.String(100), nullable=False)
    description = sq_database.Column(sq_database.String(500))
    price = sq_database.Column(sq_database.Float, nullable=False)
    quantity = sq_database.Column(sq_database.Integer, nullable=False)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

#Defining Toy Table Schema
class ToySchema(Schema):
    unique_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)

toy_schema = ToySchema()
toys_schema = ToySchema(many=True)

#Configuring the Rot to Flask API
@api_object.route('/')
def home():
    return 'This is Toy Store Catalog API'

#The below function is used to Create an API for Create the Toy in the table
@api_object.route('/toys', methods=['POST'])
def create_toy():
    """
    The Function will create a toy, before doing that it will do a check by concatination of Name, Desc and Price, 
    if the toy is availabe, it will not create.
    Input:
        name(str) ex:ToyName
        description(str) ex: ToyDescrption
        price(float) ex:19.99
        quantity(int) ex:10
    Returns:
        409 and Message if toy already exists
        201 if toy is created
        400 if any validation error
        500 if there is an issue with data base
    """
    try:
        toy_schema = ToySchema()
        toy_data = request.json
        existing_toy = Toy.query.filter_by(name=toy_data['name'], description=toy_data['description'], price=toy_data['price']).first()
        if existing_toy:
            return jsonify({'message': f'Toy already existis with the displayed infomation. Please perform an update if needed.'},toy_schema.dump(existing_toy)), 409
        toy = Toy(name=toy_data['name'], description=toy_data['description'], price=toy_data['price'], quantity=toy_data['quantity'])
        sq_database.session.add(toy)
        sq_database.session.commit()
        return jsonify({'message':'Toy Created Successfully'}, toy_schema.dump(toy)), 201
    except ValidationError as e:
        return jsonify({'message': 'Invalid data', 'errors': e.messages}), 400
    except SQLAlchemyError as e:
        sq_database.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

#The below function is to get the list of all toys available
@api_object.route('/toys', methods=['GET'])
def get_toys():
    """
    This Function will get all the toys from Data Base, pagenation included
    Returns
        200 and result of data if success
        500 if database and if anyother error
    """
    try:
        page = request.args.get('page', default=1, type=int) ##creating pages, default is 1, can change at api call
        per_page = request.args.get('per_page', default=10, type=int)##creating items per page, by default 10, can change at api call

        toys = Toy.query.paginate(page=page, per_page=per_page)
        total_items = toys.total
        total_pages = toys.pages

        toy_schema = ToySchema(many=True)
        result = toy_schema.dump(toys.items)

        ##result will be displayed as below in api call
        response = {
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'toys': result
        }

        return jsonify(response), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

#The function is to get the specific toy
@api_object.route('/toys/<int:toy_id>', methods=['GET'])
def get_toy(toy_id):
    """
    This function will get the toy with ID as input
    Input:
        Toy_ID (Int, ex - 1)
    Returns:
        Toy Details, 200, if sucess
        404 if not found
        500 if database and if anyother error   
    """
    try:
        toy = Toy.query.get(toy_id)
        if toy:
            return jsonify({'message':f'Toy Found with ID - {toy_id}'}, toy_schema.dump(toy)), 200
        else:
            return jsonify({'message': f"Toy not found with ID - {toy_id}"}), 404
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

#The function is to update the Toy using ID
@api_object.route('/toys/<int:toy_id>', methods=['PUT'])
def update_toy(toy_id):
    """
    This Fucntion will update toy information with the ToyID, before it will check for Toy, if exists will update
    Input:
        id(int) - ex:1
    Returns:
        200, Updated Toy Information
        400, Validation Error
        500, Database error
    """
    try:
        toy = Toy.query.get(toy_id)
        if not toy: ##checking if toy exists or not
            return jsonify({'message': f'Toy not found with ID - {toy_id}'}), 404
        updated_data = request.json
        toy.name = updated_data.get('name', toy.name)
        toy.description = updated_data.get('description', toy.description)
        toy.price = updated_data.get('price', toy.price)
        toy.quantity = updated_data.get('quantity', toy.quantity)
        sq_database.session.commit()
        result = toy_schema.dump(toy)
        return jsonify({'message':f'Toy Updated, ID - {toy_id}'}, result), 200
    except ValidationError as e:
        return jsonify({'message': 'Invalid data', 'errors': e.messages}), 400
    except SQLAlchemyError as e:
        sq_database.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

#Delte a toy with ID
@api_object.route('/toys/<int:toy_id>', methods=['DELETE'])
def delete_toy(toy_id):
    """
    This Fucntion will delete a Toy with its ID,  first will check whether the toy is there or not,
    Input:
        ID(Int) Ex - 1
    Returns:
        200, Message and deleted toys information,
        500 if database error
    """
    try:
        toy = Toy.query.get(toy_id)
        if not toy:
            return jsonify({'message': f'Toy not found with ID - {toy_id}'}), 404

        sq_database.session.delete(toy)
        sq_database.session.commit()

        return jsonify({'message': f'Toy with ID {toy_id} deleted successfully, below are the deleted information'}, toy_schema.dump(toy)), 200
    except SQLAlchemyError as e:
        sq_database.session.rollback()
        return jsonify({'message': 'Database error', 'error': str(e)}), 500

##The below function is used to search the Toy with name
@api_object.route('/toys/search', methods=['GET'])
def search_toy():
    """
    This function will search the toys by searching with name
    Input:
        Name(Str) Ex: Toy
    Returns:
        200, Will display the list fo search results,
        500 if data base error and anyother error
    """
    try:
        name = request.args.get('name', '')
        toys = Toy.query.filter(Toy.name.like(f'%{name}%')).all()
        if not toys:
            return jsonify({'message': f'No toys found with the name - {name}'}), 404
        toy_schema = ToySchema(many=True)
        result = toy_schema.dump(toys)

        return jsonify({'message': f'Toys with the search - {name} list is displayed'}, result), 200
    except SQLAlchemyError as e:
        return jsonify({'message': 'Database error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

@api_object.route('/toys', methods=['DELETE'])
def delete_all_toys():
    """
    This function will clean the table
    Returns:
        204, If success
        500, If database error, any other errors
    """
    try:
        Toy.query.delete()
        sq_database.session.commit()
        return jsonify({'message': 'All toys in the database deleted successfully'}), 200
    except SQLAlchemyError:
        sq_database.session.rollback()
        return jsonify({'error': 'Database Error'}), 500
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

if __name__ == '__main__':
    with api_object.app_context():
        sq_database.create_all()
    api_object.run(debug=True)

print("Running")
