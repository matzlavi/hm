from pymongo import MongoClient
from flask import Flask, request, jsonify
import json
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__, static_folder="../static", static_url_path="/static")

def to_json(obj):
	return json.dumps(obj, default=json_util.default)

def get_mongo_client():
	client = MongoClient()
        db = client.hire_db
        collection = db.candidates
	return collection

@app.route('/candidates/<cid>', methods=["DELETE"])
def deleteCandidate(cid):
	col = get_mongo_client()
	col.remove({'_id':ObjectId(cid)})
	return jsonify( { 'result': True } )

@app.route('/candidates', methods=["POST"])
def insertCandidate():
	if not request.json:
		abort (400)
	data = request.json
	_id = data['_id']
	client = MongoClient()
        db = client.hire_db
        collection = db.candidates
	print _id
	if _id == "":
		del data['_id']
		collection.insert(data)
	else:
		data['_id'] = ObjectId(_id)
		collection.update({'_id':ObjectId(_id)}, data, True)

	return "{}"

@app.route('/candidates', methods=["GET"])
def getCandidates():
	print request.args
	page = request.args.get('page')
	rows_in_page = request.args.get('rows')
	sort_col = request.args.get('sidx')
	sort_order = 1
	if (request.args.get('sord') == 'desc'):
		sort_order = -1
	print page
	print rows_in_page
	print sort_col
	print sort_order
	
	client = MongoClient()
	db = client.hire_db
	collection = db.candidates
	#data = collection.find().skip((int(page)-1)*int(rows_in_page)).limit(int(rows_in_page)).sort(sort_col,direction=sort_order)
	data = collection.find().sort(sort_col,direction=sort_order)
	result="["
	for d in data:
		if (result != "["):
			result = result + ','
		result = result + to_json(d)

	return result + "]"

if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0')
