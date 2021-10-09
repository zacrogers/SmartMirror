from ipaddress import IPv4Address
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from typing import List

from node_types import NodeType, Node, SensorNode, PowerStripNode

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db  = SQLAlchemy(app)

class NodeModel(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    label     = db.Column(db.String(10), unique=True, nullable=False)
    ip_addr   = db.Column(db.String(15), unique=True, nullable=False)
    node_type = db.Column(db.String(10), nullable=False)

    def __repr__(self) -> str:
        return f"id:{self.id}, label:{self.label}, ip:{self.ip_addr}, type:{self.node_type}"


# db.create_all()

# n = NodeModel(label="BedroomSensor", ip_addr="192.168.2.0", node_type="SENSOR")
# db.session.add(n)
# db.session.commit()

# n = NodeModel(id=2, label="LoungeSensor", ip_addr="192.168.2.6", node_type=NodeType.SENSOR)
# db.session.add(n)
# db.session.commit()

node_add_args = reqparse.RequestParser()
node_add_args.add_argument("label", type=str, help="Label for node is required.", required=True)
node_add_args.add_argument("ip_addr", type=str, help="IP address for node is required.", required=True)
node_add_args.add_argument("type", type=str, help="Type of node is required.", required=True)

resource_fields = {
    'id': fields.Integer,
    'label': fields.String,
    'ip_addr': fields.String,
    'node_type':fields
}

nodes = {}


class HelloWorld(Resource):
    def get(self):
        return {"data":"The server is alive!"}


class ManageNode(Resource):

    @marshal_with(resource_fields)
    def put(self, label):
        args = node_add_args.parse_args()
        result = NodeModel.query.filter_by(label=label).first()
        
        if result:
            abort(409, message="Node of type {node_type} called {label} already exists. Node labels must be unique.")

        node = NodeModel(label=args["label"], ip_addr=args["ip_addr"], node_type=args["type"])
        db.session.add(node)
        db.session.commit()

        return node, 201

    def get(self, label:str):
        return {"It worked with only 1 arg":""},405

    def delete(self, label:str):
        # args = node_add_args.parse_args()
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            return 404

        db.session.delete(result)
        db.session.commit()

        return 200


class UpdateNode(Resource):
    def patch(self):
        return {"data":"The server is alive!"}


class Sensor(Resource):
    def get(self, label):
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            return 204

        node = SensorNode(result.label, IPv4Address(result.ip_addr))
        # return node.get_data(), 200
        return {"light":result.label, "temperature":result.ip_addr, "humidity":result.node_type}, 200
        
    # def get(self, label):
    #     if label not in nodes:
    #         abort(404, message=f"No sensor node called {label} exists.")

    #     node = nodes[label]
    #     return node.get_data()


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
api.add_resource(ManageNode, "/manage_node/<string:label>")
# api.add_resource(UpdateNode, "/node/<string:label>/<string:ip_addr>/<string:type>")
api.add_resource(Sensor, "/sensor/<string:label>")
api.add_resource(Power, "/power/<string:label>")
# api.add_resource(DoorLock, "/doorlock/<ip_addr>")


if __name__ == "__main__":
    app.run(debug=True)