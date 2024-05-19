#!/bin/python3

from flask import Flask, render_template, make_response
from dotenv import load_dotenv
from app.certificate_verifier import CertificateVerifier
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
	
	session_id = get_session_id()
	uploadfile('cert', session_id)
	if os.path.getsize('/tmp/' + session_id + '/cert.pem') == 0:
		return render_template('layout.html', message="ERROR: Certificate not selected", env=env)

	uploadfile('privkey', session_id)
	if os.path.getsize('/tmp/' + session_id + '/privkey.pem') == 0:
		return render_template('layout.html', message="ERROR: Private Key not selected", env=env)
	
	uploadfile('chain', session_id)
	if os.path.getsize('/tmp/' + session_id + '/chain.pem') == 0:
		return render_template('layout.html', message="ERROR: Intermediate Certificate not selected", env=env)

	cv = CertificateVerifier('/tmp/' + session_id + '/cert.pem', '/tmp/' + session_id + '/privkey.pem', '/tmp/' + session_id + '/chain.pem')
	res = cv.verify_certificate_integrity()

	for tmpfile in glob.glob('/tmp/' + session_id + '/*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res, result_title="Execution Result", env=env)

def uploadfile(type, session_id):
	"""
	Save the files in the request

	Parameters
	----------
	type : string

	Returns
	-------
	None
	"""
	dir_path = '/tmp/' + session_id
	os.makedirs(dir_path, exist_ok=True)

	file = flask.request.files[type]
	file.save('/tmp/' + session_id + '/' + type + '.pem')

def get_session_id():
	"""
	Get Session ID

	Parameters
	----------
	None

	Returns
	-------
	session_info['id']: string
	"""
	session_info = flask.request.cookies.get('id')
	if session_info is not None:
		session_info = json.loads(session_info)
	return session_info['id']

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
