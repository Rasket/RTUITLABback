from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)

class Products(Resource):
    def get(self):
        id_by = request.args.get('id', None)
        shop = request.args.get('shop', None)
        product = request.args.get('product', None)
        product = str(product)
        amount  = request.args.get('amount', None)
        pay_type  = request.args.get('pay_type', None)
        t = Product.query.filter_by(name = product).first()
        s = Shop.query.filter_by(name = shop).first()
        db.session.commit()
        if t.shop_id == s.id:
            if t.amount >= int(amount):
                t.amount -= int(amount)
                db.session.commit()
                temp_check = Check(id_buy = id_by, date = datetime.utcnow()
                , cost = t.cost*int(amount), category = s.category, type_pay = pay_type)
                db.session.add(temp_check)
                db.session.commit()
                return 'Buy'
            else:
            	return 'Out of product'
        
    def post(self):
        pass

'''
Models
'''
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    shop_id = db.Column(db.Integer)
    name = db.Column(db.String(120))
    description = db.Column(db.String(250))	
    cost = db.Column(db.Integer)
    amount = db.Column(db.Integer)

    def jsoni(self):
    	return jsonify(id = self.id, shop=self.shop_id, name=self.name,
    		description=self.description, cost=self.cost, amount=self.amount)
    def __repr__(self):
        return f'<Product {self.name} {self.description} {self.amount}>'

class Check(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_buy = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    cost = db.Column(db.Integer)
    category = db.Column(db.String(140))
    type_pay = db.Column(db.String(140))

'''
End of models
'''



api.add_resource(Products, "/api/products")


@app.route('/check/<id>', methods=['GET'])
def getcheck(id):
    u = Check.query.filter_by(id_buy = id).all()    
    '''
    ida = []
    id_buy = []
    date = []
    cost = []
    category = []        
    type_pay = []
    for i in u:
        ida.append(i.id)
        id_buy.append(i.id_buy)
        date.append(i.date)
        category.append(i.category)
        cost.append(i.cost)
        type_pay.append(i.type_pay)
    return jsonify(id = ida, id_buy=id_buy, date=date,
    		category=category, cost=cost, type_pay=type_pay)
    '''
    ret = {}
    key = 0
    for i in u:
        ret[key] = {'id' : i.id, 'id_buy' : i.id_buy, 'date' : i.date,
            'category' : i.category, 'cost' : i.cost, 'type_pay' : i.type_pay}
        key += 1
    return jsonify(ret)
if __name__ == "__main__":
	app.run(debug=True)