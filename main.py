from models import *
from flask_httpauth import HTTPBasicAuth
from flask import abort, request, jsonify, g, url_for
auth = HTTPBasicAuth()
# route to get all locations
@app.route('/locations', methods=['GET'])
@auth.login_required
def get_locations():
    print(request)
    '''Function to get all the locations in the database'''
    return jsonify({'Locations': Location.get_all_locations()})


# route to get location by id
@app.route('/location/<int:id>', methods=['GET'])
def get_location_by_id(id):
    return_value = Location.get_location(id)
    return jsonify(return_value)


# route to get department by location id
@app.route('/location/<int:id>/department', methods=['GET'])
def get_dept_by_loc_id(id):
    return_value = Department.get_department_by_loc(id)
    return jsonify(return_value)


# route to get category by department_id and location id
@app.route('/location/<int:locid>/department/<int:depid>/category', methods=['GET'])
def get_category_by_dept_and_loc_id(locid, depid):
    return_value = Department.get_category_by_dept_and_loc_id(locid, depid)
    return jsonify(return_value)


# route to add new location
@app.route('/locations', methods=['POST'])
def add_location():
    '''Function to add new location to our database'''
    request_data = request.get_json()  # getting data from client
    print(request_data)
    Location.add_location(request_data["name"], request_data["description"])
    response = Response("Location added", 201, mimetype='application/json')
    return response


# route to update location with PUT method
@app.route('/locations/<int:id>', methods=['PUT'])
def update_location(id):
    '''Function to edit location in our database using location id'''
    request_data = request.get_json()
    Location.update_location(id, request_data['name'], request_data['description'])
    response = Response("Location Updated", status=200, mimetype='application/json')
    return response


# route to delete location using the DELETE method
@app.route('/locations/<int:id>', methods=['DELETE'])
def remove_location(id):
    '''Function to delete location from our database'''
    Location.delete_location(id)
    response = Response("Location Deleted", status=200, mimetype='application/json')
    return response


# route to get all metadata records
# @app.route('/meta', methods=['GET'])
# def get_meta():
#     print(request)
#     '''Function to get all the locations in the database'''
#     return jsonify({'Metadata': Metadata.get_all_metadata()})


# route to get metadata based on id
@app.route('/meta/<int:id>', methods=['GET'])
@auth.login_required
def get_meta_by_id(id):
    '''Function to get all the locations in the database'''
    return jsonify({'Metadata': Metadata.get_metadata(id)})


# route to add new metadata record
@app.route('/metadata', methods=['POST'])
def add_meta():
    '''Function to add new location to our database'''
    request_data = request.get_json()  # getting data from client
    print(request_data)
    Metadata.add_meta(request_data["location_id"], request_data["department_id"],
                      request_data["category_id"], request_data["sub_category_id"])
    response = Response("Metadata added", 200, mimetype='application/json')
    return response


# route to update location with PUT method
@app.route('/meta', methods=['PUT'])
def update_meta():
    '''Function to edit location in our database using location id'''
    request_data = request.get_json()
    Location.update_meta(id, request_data['name'], request_data['description'])
    response = Response("Metadata Updated", status=200, mimetype='application/json')
    return response


# route to delete location using the DELETE method
@app.route('/meta/<int:id>', methods=['DELETE'])
def remove_meta(id):
    '''Function to delete location from our database'''
    Metadata.delete_location(id)
    response = Response("Metadata Deleted", status=200, mimetype='application/json')
    return response


@auth.verify_password
def verify_password(username_or_token, password):
    # first try token
    user = User.verify_auth_token(username_or_token)
    # then check for username and password pair
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    # Check for blank requests
    if username is None or password is None:
        abort(400)
    # Check for existing users
    if User.query.filter_by(username = username).first() is not None:
        abort(400)
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)


@app.route('/api/login')
@auth.login_required
def get_token():
    # username = request.json.get('username')
    # password = request.json.get('password')
    token = g.user.generate_auth_token(600)
    return jsonify({ 'token': token.decode('ascii'), 'duration': 600 })


@app.route('/api/dothis', methods=['GET'])
@auth.login_required
def do_this():
    return jsonify({ 'message':'It is done {}'.format(g.user.username) })


if __name__ == "__main__":
    app.run(port=1234, debug=True)