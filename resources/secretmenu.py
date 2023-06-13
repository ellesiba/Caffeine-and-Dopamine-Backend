import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


menu = Blueprint('secret_menu', 'menu')

@menu.route('/', methods=["GET"])
def get_all_menu():
    try:
        secret_menu = [model_to_dict(menu) for menu in models.SecretMenu.select()]
        print(secret_menu)
        return jsonify(data=secret_menu, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@menu.route('/', methods=["POST"])
def create_item():
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
