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
	work_dir = '/tmp/' + session_id + '/'

	uploadfile(work_dir, 'cert')
	if os.path.getsize(work_dir + 'cert.pem') == 0:
		return render_template('layout.html', message="ERROR: Certificate not selected", env=env)

	uploadfile(work_dir, 'privkey')
	if os.path.getsize(work_dir + 'privkey.pem') == 0:
		return render_template('layout.html', message="ERROR: Private Key not selected", env=env)
	
	uploadfile(work_dir, 'chain')
	if os.path.getsize(work_dir + 'chain.pem') == 0:
		return render_template('layout.html', message="ERROR: Intermediate Certificate not selected", env=env)

	cv = CertificateVerifier(work_dir + 'cert.pem', work_dir + 'privkey.pem', work_dir + 'chain.pem')
	res = cv.verify_certificate_integrity()

	for tmpfile in glob.glob(work_dir + '*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res, result_title="Execution Result", env=env)

def uploadfile(work_dir, type):
	"""
	Save the files in the request

	Parameters
	----------
	work_dir : string
	file : string

	Returns
	-------
	None
	"""
	os.makedirs(work_dir, exist_ok=True)

	file = flask.request.files[type]
	file.save(work_dir + type + '.pem')

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