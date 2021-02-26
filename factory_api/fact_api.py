from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import threading, time
import json
import werkzeug 


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///factory_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

def transfer():
    threading.Timer(25, transfer).start()#каждый час поставка 3600 sec
    json_data = json.dumps({"shop" : "First", "product" : 
        { "1" : "first"}, "amount" : {"1":"1"}})
    try:
        r = requests.post("http://127.0.0.1:9998/api/products/", data = json_data)
        if r.text[1:-2] == 'GET':
            print('Allright')
        else:
            print('Some error occured')
    except:
    	print('No connect')




'''
Завод производит продукты на склад
С склада переодически идет проверка на доступность магазина
Если магазин доступен, то отсылаются продукты, иначе записываются на склад
'''





if __name__ == "__main__":
	if werkzeug.serving.is_running_from_reloader():
		transfer()
	else:
		pass
	app.run(port=7777, debug=True)