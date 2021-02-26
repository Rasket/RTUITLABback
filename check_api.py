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
    category = db.Column(db.String(140))# категория товара
    cost = db.Column(db.Integer)# стоимость всей покупки
    type_pay = db.Column(db.String(140))# способ оплаты
    date = db.Column(db.DateTime, default = datetime.utcnow)# дата по Гринвичу

class Check(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		print(json_data)
		return json_data
		id_buy = json_data['id']
		shop = json_data['shop']
		products = json_data['products']
		amounts = json_data['amounts']
		type_pay = json_data['type_pay']   
		temp_check = Check(id_buy = id_buy, date = datetime.utcnow(), products = temp_prod, amounts = temp_amount
				, cost = cost, category = s.category, type_pay = type_pay)
		db.session.add(temp_check)
		db.session.commit()


api.add_resource(Check, "/getcheck/")
	
@app.route("/getcheck/<int:id>", methods=['GET'])
def index(id):
	id = str(id)
	data = requests.get('http://0.0.0.0:80/check/', data = json.dumps({"id":id}))
	json_data = json.loads(data.text)
	return render_template("base.html", data=json_data)

if __name__ == "__main__":
	app.run(port=8888, debug=True)
