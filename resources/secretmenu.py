import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


menu = Blueprint('secret_menu', 'menu')

# index
@menu.route('/', methods=["GET"])
def get_all_menu():
    try:
        secret_menu = [model_to_dict(menu) for menu in models.SecretMenu.select()]
        print(secret_menu)
        return jsonify(data=secret_menu, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#Create Route
@menu.route('/', methods=["POST"])
def create_menu():
    payload = request.get_json()
    try:
        menu = models.SecretMenu.create(**payload)
        print(menu.__dict__)
        print(dir(menu))
        print(model_to_dict(menu), 'model to dict')

        menu_dict = model_to_dict(menu)
        return jsonify(data=menu_dict, status={"code": 201, "message": "Success"})
    except Exception as e:
        return jsonify(data={}, status={"code": 500, "message": "Error creating the item: " + str(e)})

#Show Route
@menu.route('/<id>', methods=["GET"])
def get_one_menu(id):
    menu = models.SecretMenu.get_by_id(id)
    print(menu.__dict__)
    return jsonify(
        data=model_to_dict(menu),
        status= 200,
        message="Success"
    ), 200


#Update Route
@menu.route('/<id>', methods=["PUT"])
def update_menu(id):
    payload = request.get_json()
    query = models.SecretMenu.update(**payload).where(models.SecretMenu.id == id)
    query.execute()
    return jsonify(
        data=model_to_dict(models.SecretMenu.get_by_id(id)),
        status=200,
        message='Resource updated successfully'
    )

# Delete
@menu.route('/<id>', methods=["Delete"])
def delete_menu(id):
    query = models.SecretMenu.delete().where(models.SecretMenu.id==id)
    query.execute()
    return jsonify(
        data='resource successfully deleted',
        message= 'resource deleted successfully',
        status=200
    ), 200

