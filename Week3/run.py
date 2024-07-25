from flask import Flask, request, jsonify
import json
from flasgger import Swagger
from flasgger.utils import swag_from


flask_app = Flask(__name__)


swagger = Swagger(flask_app, config={
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
})


class FileProcessingError(Exception):
    pass


@flask_app.route('/')
@swag_from('swagger_config.yml', methods=['GET'])
def index():
    return 'Server is running'


@flask_app.route('/post', methods=['POST'])
@swag_from('swagger_config.yml', methods=['POST'])
def post_data():
    try:
        with open("data_file.json", 'r') as r:
            content = r.read()
    except FileNotFoundError as ex:
        return "Mentioned file doesn't exist"
    except Exception as ex:
        raise FileProcessingError("An error occurred while processing the file.")
    if not content:
        data = dict()
        data['Likhitha'] = 'Python'
        with open("data_file.json", 'w') as w:
            w.write(json.dumps(data))
    else:
        with open("data_file.json", 'r') as r:
            data = json.loads(r.read())
            data['Likhitha'] = 'Python'
        with open("data_file.json", 'w') as w:
            w.write(json.dumps(data))
    return "data added successfully"


@flask_app.route('/get', methods=['GET'])
@swag_from('swagger_config.yml', methods=['GET'])
def get_data():
    try:
        with open("data_file.json", 'r') as r:
            content = r.read()
    except FileNotFoundError as ex:
        return "No data present in the file"
    if content:
        data = json.loads(content)
        return data
    else:
        return "no data present in the file"


@flask_app.errorhandler(FileProcessingError)
def handle_file_processing_error(error):
    response = jsonify({"message": str(error)})
    response.status_code = 500
    return response


if __name__ == '__main__':
    flask_app.run(debug=True)