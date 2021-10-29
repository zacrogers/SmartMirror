from ipaddress import IPv4Address
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from typing import List

from node_types import NodeType, Node, SensorNode, PowerStripNode

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class NodeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(10), unique=True, nullable=False)
    ip_addr = db.Column(db.String(15), unique=True, nullable=False)
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

node_info_args = reqparse.RequestParser()
node_info_args.add_argument("get_all_labels", type=str)

node_put_args = reqparse.RequestParser()
node_put_args.add_argument(
    "label", type=str, help="Label for node is required.", required=True
)
node_put_args.add_argument(
    "ip_addr", type=str, help="IP address for node is required.", required=True
)
node_put_args.add_argument(
    "type", type=str, help="Type of node is required.", required=True
)

node_patch_args = reqparse.RequestParser()
node_patch_args.add_argument(
    "new_label", type=str, help="Label for node is required.", required=True
)
node_patch_args.add_argument("ip_addr", type=str, required=False)

pwr_node_put_args = reqparse.RequestParser()
pwr_node_put_args.add_argument(
    "channel", type=int, help="Channel for power node is required.", required=True
)
pwr_node_put_args.add_argument(
    "state", type=bool, help="State for power node is required.", required=True
)

resource_fields = {
    "id": fields.Integer,
    "label": fields.String,
    "ip_addr": fields.String,
    "node_type": fields.String,
}


class NodeInfo(Resource):
    def get(self):
        args = node_info_args.parse_args()

        if "get_all_labels" in args.keys():
            node_labels = {
                i: node.label for i, node in enumerate(NodeModel.query.all())
            }

        return node_labels, 200


class ManageNode(Resource):
    @marshal_with(resource_fields)
    def put(self, label: str):
        args = node_put_args.parse_args()
        result = NodeModel.query.filter_by(label=label).first()

        if result:
            abort(
                409,
                message="Node of type {node_type} called {label} already exists. Node labels must be unique.",
            )

        node = NodeModel(
            label=args["label"], ip_addr=args["ip_addr"], node_type=args["type"]
        )
        db.session.add(node)
        db.session.commit()

        return node, 201

    @marshal_with(resource_fields)
    def get(self, label: str):
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            abort(404, message="Node called {label} doesn't exist.")

        node = NodeModel(
            label=result.label, ip_addr=result.ip_addr, node_type=result.node_type
        )

        return node, 200

    def delete(self, label: str):
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            abort(404, message="Node called {label} doesn't exist.")

        db.session.delete(result)
        db.session.commit()

        return 200

    def patch(self, label: str):
        args = node_patch_args.parse_args()
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            abort(404, message="Node called {label} doesn't exist.")

        result.label = args["new_label"]

        if "ip_addr" in args.keys():
            result.ip_addr = args["ip_addr"]

        db.session.merge(result)
        db.session.commit()

        return 200


class Sensor(Resource):
    def get(self, label: str):
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            return 204

        node = SensorNode(result.label, IPv4Address(result.ip_addr))
        return node.get_data(), 200
        # return {"light":result.label, "temperature":result.ip_addr, "humidity":result.node_type}, 200


class Power(Resource):
    def get(self, label: str):
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            return 404

        node = PowerStripNode(result.label, IPv4Address(result.ip_addr))
        states = node.get_states()

        return states, 200

    def put(self, label: str):
        pwr_node_put_args.parse_args()
        result = NodeModel.query.filter_by(label=label).first()

        if not result:
            return 404

        node = PowerStripNode(result.label, IPv4Address(result.ip_addr))

        if result["state"] == True:
            node.channel_on(result["channel"])
        else:
            node.channel_off(result["channel"])

        states = node.get_states()

        return states, 200


class DoorLock(Resource):
    def put(self, label: str):
        return {"data": "Hello world"}


api.add_resource(NodeInfo, "/node_info")
api.add_resource(ManageNode, "/manage_node/<string:label>")
api.add_resource(Sensor, "/sensor/<string:label>")
api.add_resource(Power, "/power/<string:label>")
api.add_resource(DoorLock, "/doorlock/<string:label>")


if __name__ == "__main__":
    app.run(debug=True)
