from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource
import requests
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///check_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# percent encode
# url request with json //optional, ask a questidon.
api = Api(app)

class Check(db.Model):# модель Чеков
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_buy = db.Column(db.Integer)# id покупателя
    products = db.Column(db.String(500))
    amounts = db.Column(db.Integer)
    shop = db.Column(db.String(240))
    category = db.Column(db.String(140))# категория товара
    cost = db.Column(db.Integer)# стоимость всей покупки
    type_pay = db.Column(db.String(140))# способ оплаты
    date = db.Column(db.String)# дата по Гринвичу

class Check_api(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		id_buy = json_data['id_buy']
		shop = json_data['shop']
		products = json_data['products']
		amounts = json_data['amounts']
		type_pay = json_data['type_pay']
		data = json_data['data']
		cost = json_data['cost']
		category = json_data['category']
		temp_check = Check(id_buy = id_buy, shop = shop, date = data, products = products, amounts = amounts
				, cost = cost, category = category, type_pay = type_pay)
		db.session.add(temp_check)
		db.session.commit()


api.add_resource(Check_api, "/getcheck/")
	
@app.route("/getcheck/<int:id>", methods=['GET'])
def index(id):
    id = str(id)

    try:
        r = requests.get("http://shop:9998/api/getcheck/")
    except:
        print('Some troubles')
    u = Check.query.filter_by(id_buy = id).all()    
    ret = {}# словарик, в который пишутся все чеки
    key = 0# ключик словарика
    for i in u:
        ret[key] = {'id' : i.id, 'id_buy' : i.id_buy, 'date' : i.date, 'products' : i.products, "amounts" : i.amounts,
            'category' : i.category, 'cost' : i.cost, 'type_pay' : i.type_pay}# вытаскиваем поля из записей
        key += 1
    #json_data = json.loads(ret)
    return render_template("base.html", data=ret)

if __name__ == "__main__":
    session = requests.Session()
    session.trust_env = False
    app.run(host="0.0.0.0", port=8888, debug=True)
