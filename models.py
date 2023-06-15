from peewee import *
from flask_cors import CORS
CORS(origins=['http://localhost:3000'], supports_credentials=True) 


DATABASE = SqliteDatabase('secret_menu.sqlite')

class SecretMenu(Model):
    name = CharField()
    coffee = BooleanField()
    tea = BooleanField()
    milk = BooleanField()
    additional_flavors = CharField()
    taste_profile = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([SecretMenu], safe=True)
    print("TABLES Created")
    DATABASE.close()

# Call initialize() to create the tables
initialize()
