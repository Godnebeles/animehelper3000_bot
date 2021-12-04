from flask import Flask, request
import sys
from .. import YummyParser

print(sys.path)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return request.args.get('title')


app.run()


