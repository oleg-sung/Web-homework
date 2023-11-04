from flask import Flask


app = Flask('app')
from app import models, routs, views, schema, errors

if __name__ == '__main__':
    app.run()
