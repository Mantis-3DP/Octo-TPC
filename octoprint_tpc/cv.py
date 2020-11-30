import sys
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')



def double(number):

	sum = int(number) + int(number)
	return sum


def add(number, number2):
	sum = int(number) + int(number2)
	return sum

@app.route('/sleep')
def sleep():
	time.sleep(10)
	mystatus = "200 OK"
	sys.stdout.write("Status: %s\n" % mystatus)


if __name__ == "__main__":
    app.run()
