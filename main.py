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
  
	certificate_fs = flask.request.files['certificate']
	certificate_fs.save('./certificate.crt')
	privatekey_fs = flask.request.files['privatekey']
	privatekey_fs.save('./privatekey.key')
	intermediate_fs = flask.request.files['intermediate']
	intermediate_fs.save('./intermediate.ca')

	res = subprocess.run('./app/cert_check.sh ./certificate.crt ./privatekey.key ./intermediate.ca', shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	# 一時ファイルを削除
	#for tmpfile in glob.glob('./*'):
	#	os.remove(tmpfile)
	#for crtfile in glob.glob('./*'):
	#	os.remove(crtfile)

	#return res.stdout.decode("utf8")
	mes = res.stdout.decode("utf8")
	return render_template('layout.html', result=mes, restitle="実行結果")

if __name__ == "__main__":
	app.run(host='0.0.0.0')
	
