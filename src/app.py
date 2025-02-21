"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")  # Create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET', 'POST'])
def handle_hello():
    response_body = {}
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        response_body['hello'] = "world"
        response_body['family'] = members
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        jackson_family.add_member(data)
        members = jackson_family.get_all_members()
        response_body['family'] = members
        response_body['message'] = 'Nuevo integrante de la familia agregado'
        return response_body, 200

@app.route('/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def member(id):
    response_body = {}
    if request.method == 'GET':
        row = jackson_family.get_member(id)
        if row:
            response_body['results'] = row
            response_body['message'] = 'Integrante encontrado'
            return response_body, 200
        response_body['message'] = f'Integrante con id {id} no encontrado'
        return response_body, 402
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        rows = jackson_family.delete_member(id)
        response_body['family'] = rows
        response_body['message'] = f'Integrante con id {id} eliminado'
        return response_body, 200
    

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
