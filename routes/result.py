from  flask import  Blueprint, request, jsonify
result = Blueprint('result',__name__)
from services.result import ResultService

@result.route('/generate_result',methods=["POST"])
def generate_result():
    return