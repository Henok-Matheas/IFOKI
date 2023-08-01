from flask import Blueprint, jsonify, request
from chat import load_chat
import logging

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@main_bp.route('/api/chat', methods=['POST'])
def index():
    data = request.json
    response = {
        "message" : None
    }
    statusCode = 404
    try:
        address = request.headers.get('CF-Connecting-IP')
        if not address:
            # The header is not present, so use the remote address instead
            address = request.remote_addr
        if not address:
            raise Exception("Couldn't parse your IP Address")
        
        conversation = load_chat(address)
        message = data['prompt']

        output = conversation.predict(input=message)
        logging.info(output)
        response['message'] = output
        statusCode = 200
    except Exception as error:
        logging.error(error)
        response['message'] = error
        statusCode = 404

    return jsonify(response), statusCode


@main_bp.route('/api/health', methods=['GET'])
def health_check():
    response = {'status': 'ok'}
    return jsonify(response), 200