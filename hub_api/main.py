from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from typing import List

from node_types import NodeType, Node, SensorNode, PowerStripNode

app = Flask(__name__)
api = Api(app)
db  = SQLAlchemy(app)


class DbNode(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    label     = db.Column(db.String(100))
    ip_addr   = db.Column(db.String(100), unique=True)
    node_type = db.Column(db.String(100))


req_parser = reqparse.RequestParser()
nodes = List[Node]


class HelloWorld(Resource):
    def get(self):
        return {"data":"The server is alive!"}


class Sensor(Resource):
    def get(self):
        return {"data":"Hello world"}


class Power(Resource):
    power_default = {"light":"99", "temperature":"99", "humidity":"99"}

    def get(self):
        return {"data":"Hello world"}

    def post(self):
        return NotImplementedError

# class DoorLock(Resource):
#     def get(self):
#         return {"data":"Hello world"}

api.add_resource(HelloWorld, "/")
api.add_resource(Sensor, "/sensor/<ip_addr>")
api.add_resource(Power, "/power/<ip_addr>")
# api.add_resource(DoorLock, "/doorlock/<ip_addr>")


if __name__ == "__main__":
    app.run(debug=True)