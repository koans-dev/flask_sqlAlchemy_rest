from pickle import TRUE
from unicodedata import name
from unittest import result
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os 

#Init app 
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir,'db.sqlite')
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)

# marshmallow init 

ma = Marshmallow(app)
class Product(db.Model):
    id = db.Column (db.Integer, primary_key =True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self,name,description,price,qty) :
   
        self.name = name
        self.description =description
        self.price = price
        self.qty = qty 

db.create_all()        
class ProductSchema(ma.Schema):
        class Meta:
            model = Product
            fields =('id','name','description','price','qty')

product_schema = ProductSchema()
products_schemas = ProductSchema(many=True)

@app.route('/product', methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    
    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schemas.dump(all_products)
  return jsonify(result)

  #Get single product 

@app.route('/product/<id>', methods=['GET'])
def product(id):
  product = Product.get(id)
  return product_schema.jsonify(product)
    
if __name__ =='__main__':
    app.run(debug=True)

