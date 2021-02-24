from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource
import requests
import json


app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# percent encode
# url request with json //optional, ask a question.
api = Api(app)


class Check(Resource):
	def get(self, id):
		pass

#api.add_resource(Check, "/getcheck/<int:id>")
	
@app.route("/getcheck/<int:id>", methods=['GET'])
def index(id):
	id = str(id)
	data = requests.get('http://0.0.0.0:80/check/', data = json.dumps({"id":id}))
	json_data = json.loads(data.text)
	return render_template("index.html", data=json_data)

if __name__ == "__main__":
	app.run(port=8888, debug=True)
