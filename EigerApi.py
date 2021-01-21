from flask import Flask, json, request
from flask_cors import CORS, cross_origin

from EigerMockStructure import EigerCommand


class EigerApi:
    def __init__(self, eiger):
        self._app = Flask(__name__)
        cors = CORS(self._app)
        self._app.config["CORS_HEADERS"] = "Content-Type"
        self._eiger = eiger
        self.set_up_routes()

    def set_up_routes(self):
        @self._app.route("/<module>/api/<version>/<task>", methods=["GET"])
        @self._app.route("/<module>/api/<version>/<task>/", methods=["GET"])
        @cross_origin()
        def get_task(module=None, version=None, task=None):
            eiger_module = getattr(self._eiger, module)
            eiger_task = getattr(eiger_module, task)
            return eiger_task.get()

        @self._app.route("/<module>/api/<parameter>", methods=["GET"])
        @self._app.route("/<module>/api/<parameter>/", methods=["GET"])
        @cross_origin()
        def get_version(module=None, task=None, parameter=None):
            eiger_module = getattr(self._eiger, module)
            eiger_parameter = getattr(eiger_module, parameter)
            return eiger_parameter.get()

        @self._app.route(
            "/<module>/api/<version>/<task>/<parameter>", methods=["GET", "PUT"]
        )
        def get_parameter(module=None, version=None, task=None, parameter=None):
            eiger_module = getattr(self._eiger, module)
            eiger_task = getattr(eiger_module, task)
            eiger_parameter = getattr(eiger_task, parameter)
            if request.method == "GET":
                return json.dumps(eiger_parameter.get())
            else:
                print("received a put request...")
                if isinstance(eiger_parameter, EigerCommand):
                    return json.dumps(eiger_parameter())
                else:
                    return json.dumps(eiger_parameter.put(request.json))

    def run(self):
        self._app.run()


if __name__ == "__main__":
    api = EigerApi(None)
    api.run()