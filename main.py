#!/bin/python3

from flask import Flask, render_template
import flask
import subprocess
import os
import glob
app = Flask(__name__)

@app.route('/')
def lambda_handler(event=None, context=None):
	return render_template('layout.html')

@app.route('/exec', methods=['POST'])
def exec():
	
	cert_fs = flask.request.files['cert']
	cert_fs.save('/tmp/cert.pem')

	if os.path.getsize('/tmp/cert.pem') == 0:
		return render_template('layout.html', message="Error: Certificate not selected")
	
	privkey_fs = flask.request.files['privkey']
	privkey_fs.save('/tmp/privkey.pem')

	if os.path.getsize('/tmp/privkey.pem') == 0:
		return render_template('layout.html', message="Error: Private key not selected")
	
	chain_fs = flask.request.files['chain']
	chain_fs.save('/tmp/chain.pem')

	if os.path.getsize('/tmp/chain.pem') == 0:
		return render_template('layout.html', message="Error: Intermediate certificate not selected")

	res = subprocess.run('./app/cert_check.sh /tmp/cert.pem /tmp/privkey.pem /tmp/chain.pem', shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	for tmpfile in glob.glob('/tmp/*.pem'):
		os.remove(tmpfile)

	return render_template('layout.html', message=res.stdout, restitle="Execution Result<br>")

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
