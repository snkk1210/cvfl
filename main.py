#!/bin/python3

from flask import Flask, render_template
from dotenv import load_dotenv
import flask
import subprocess
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
	uploadfile('privkey')
	uploadfile('chain')

	res = subprocess.run('./app/cert_check.sh /tmp/cert.pem /tmp/privkey.pem /tmp/chain.pem', shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	for tmpfile in glob.glob('/tmp/*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res.stdout.decode("utf8"), restitle="Execution Result", env=env)

def uploadfile(type):
	file = flask.request.files[type]
	file.save('/tmp/' + type + '.pem')

	if os.path.getsize('/tmp/' + type + '.pem') == 0:
		return render_template('layout.html', message="Error: " + type + "not selected", env=env)

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
