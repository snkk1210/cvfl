#!/bin/python3

from flask import Flask, render_template
from dotenv import load_dotenv
from app.certificate_verifier import CertificateVerifier
import flask
import os
import glob

app = Flask(__name__)
load_dotenv(override=True)
env = os.getenv('ENV')

@app.route('/')
def lambda_handler(event=None, context=None):
	return render_template('layout.html', env=env)

@app.route('/exec', methods=['POST'])
def exec():
	
	uploadfile('cert')
	if os.path.getsize('/tmp/cert.pem') == 0:
		return render_template('layout.html', message="Error: Certificate not selected", env=env)

	uploadfile('privkey')
	if os.path.getsize('/tmp/privkey.pem') == 0:
		return render_template('layout.html', message="Error: Private key not selected", env=env)
	
	uploadfile('chain')
	if os.path.getsize('/tmp/chain.pem') == 0:
		return render_template('layout.html', message="Error: Intermediate certificate not selected", env=env)

	cv = CertificateVerifier("/tmp/cert.pem", "/tmp/privkey.pem", "/tmp/chain.pem")
	res = cv.verify_certificate_integrity()

	for tmpfile in glob.glob('/tmp/*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res.decode("utf8"), restitle="Execution Result", env=env)

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
	
