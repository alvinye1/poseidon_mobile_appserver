# -*- coding:utf-8 -*-
from flask import Flask, request 
import json 
def after_request(response): 
	response.headers['Access-Control-Allow-Origin'] = '*' 
	response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE' 
	response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization' 
	return response 
def create_app(): 
	app = Flask(__name__) 
	app.after_request(after_request) 

	@app.route("/Detail",methods=['POST']) 
	def add_Spec(): 
		print '新增规格' 
		data = request.get_data() 
		json_re = json.loads(data) 
		print json_re 
		return 'json_re'


if __name__ == '__main__':
	aaa = create_app()
	print aaa
	print "aaa"
