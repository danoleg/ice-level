import json
import ssl

from flask_restful import Api, Resource, reqparse
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from helpers.encoder import DateTimeEncoder
from helpers.iris import iris_connection
from importer import json_to_iris

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

app.config['iris_host'] = "iris"
app.config['iris_port'] = 1972
app.config['iris_namespace'] = "USER"
app.config['iris_username'] = "_SYSTEM"
app.config['iris_password'] = "demopass"


class ImportDataset(Resource):
    def post(self):
        global_name = "IceThickness"
        with open('data/ice-thickness.json') as f:
            data = json.load(f)
            result, iris_data = json_to_iris(json.dumps(data), global_name)
        if result:
            data = {
                "status": True,
                "message": "Imported successfully",
            }
        else:
            data = {
                "status": False,
                "message": "Invalid json",
                "data": data
            }

        return data


class SetData(Resource):
    def get(self):
        data = {
            "iris_host": app.config['iris_host'],
            "iris_port": app.config['iris_port'],
            "iris_namespace": app.config['iris_namespace'],
            "iris_username": app.config['iris_username'],
            "iris_password": app.config['iris_password']
        }
        return data


class GetData(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('year')
        post_parser.add_argument('month')
        args = post_parser.parse_args()
        global_name = "IceThickness"

        with iris_connection() as iris:
            item_data = iris.get(global_name, args.year, args.month)
        data = {
            "status": True,
            "data": item_data
        }
        return data


class GetDataByMonth(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('month')
        post_parser.add_argument('year')
        args = post_parser.parse_args()
        global_name = "IceThickness"

        values = []
        years = []
        val = 0

        with iris_connection() as iris:
            for year in range(1979, 2023):
                value = iris.get(global_name, str(year), args.month)
                if str(year) == args.year:
                    val = value
                values.append(value)
                years.append(year)
        data = {
            "status": True,
            "data": {
                "data": values,
                "years": years
            },
            "value": val
        }
        return data


class UpdateData(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('year')
        post_parser.add_argument('month')
        post_parser.add_argument('value')
        args = post_parser.parse_args()
        global_name = "IceThickness"

        with iris_connection() as iris:
            item_data = iris.set(args.value, global_name, args.year, args.month)
        data = {
            "status": True,
            "data": item_data
        }
        return data


class CheckGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('node')
        args = post_parser.parse_args()
        with iris_connection() as iris:
            iris_root_nodes_count = iris.count_root_nodes(args.name)
        data = {
            "status": True,
            "data": iris_root_nodes_count
        }

        return data


class DeleteGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        args = post_parser.parse_args()
        result = kill_iris_global(args.name)
        if result:
            data = {
                "status": True,
                "message": f"{args.name} removed successfully",
            }
        else:
            data = {
                "status": False,
                "message": "Error"
            }

        return data


class Settings(Resource):
    def get(self):
        data = {
            "iris_host": app.config['iris_host'],
            "iris_port": app.config['iris_port'],
            "iris_namespace": app.config['iris_namespace'],
            "iris_username": app.config['iris_username'],
            "iris_password": app.config['iris_password']
        }
        return data


class IRISSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('iris_host')
        post_parser.add_argument('iris_port')
        post_parser.add_argument('iris_namespace')
        post_parser.add_argument('iris_username')
        post_parser.add_argument('iris_password')
        args = post_parser.parse_args()

        try:
            connection = args.iris_host, int(args.iris_port), args.iris_namespace, args.iris_username, args.iris_password
            with iris_connection(*connection) as iris:
                pass
        except Exception as e:
            data = {
                "result": "Error",
                "details": str(e)
            }
            return data

        app.config['iris_host'] = args.iris_host
        app.config['iris_port'] = int(args.iris_port)
        app.config['iris_namespace'] = args.iris_namespace
        app.config['iris_username'] = args.iris_username
        app.config['iris_password'] = args.iris_password

        data = {
            "result": "Success"
        }
        return data

api.add_resource(ImportDataset, '/import-dataset')
api.add_resource(GetData, '/data/getting')
api.add_resource(GetDataByMonth, '/data/getting/month')
api.add_resource(UpdateData, '/data/set')
api.add_resource(DeleteGlobal, '/remove-global-from-iris')
api.add_resource(CheckGlobal, '/check-global-from-iris')
api.add_resource(IRISSettings, '/settings/iris')
api.add_resource(Settings, '/settings')


def kill_iris_global(root_item):
    with iris_connection() as iris:
        iris.kill(root_item)
    return 1

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011)
