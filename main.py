#!/bin/python3

from flask import Flask, render_template
from dotenv import load_dotenv
from app.certificate_verifier import CertificateVerifier
from flask import make_response
import flask
import os
import glob
import datetime
import json

app = Flask(__name__)
load_dotenv(override=True)
env = os.getenv('ENV')

@app.route('/')
def lambda_handler(event=None, context=None):
	max_age_sec = 300
	expires = int(datetime.datetime.now().timestamp()) + max_age_sec
	session_id = os.urandom(24).hex()
	session_info = {'id':session_id}
	resp = make_response(render_template('layout.html', env=env))
	resp.set_cookie('id', value=json.dumps(session_info), expires=expires)
	return resp

@app.route('/exec', methods=['POST'])
def exec():
	
	uploadfile('cert')
	if os.path.getsize('/tmp/cert.pem') == 0:
		return render_template('layout.html', message="ERROR: Certificate not selected", env=env)

	uploadfile('privkey')
	if os.path.getsize('/tmp/privkey.pem') == 0:
		return render_template('layout.html', message="ERROR: Private Key not selected", env=env)
	
	uploadfile('chain')
	if os.path.getsize('/tmp/chain.pem') == 0:
		return render_template('layout.html', message="ERROR: Intermediate Certificate not selected", env=env)

	cv = CertificateVerifier("/tmp/cert.pem", "/tmp/privkey.pem", "/tmp/chain.pem")
	res = cv.verify_certificate_integrity()

	for tmpfile in glob.glob('/tmp/*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res, result_title="Execution Result", env=env)

def uploadfile(type):
	"""
	Save the files in the request

	Parameters
	----------
	type : string

	Returns
	-------
	None
	"""
	file = flask.request.files[type]
	file.save('/tmp/' + type + '.pem')

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
