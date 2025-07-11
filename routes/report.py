import json
import os

from  flask import  Blueprint, request, jsonify, send_file, abort
report = Blueprint('report',__name__)
from services.report import ReportService


@report.route('/create_report', methods=['POST'])
def create_report():
    """创建报告接口"""
    data = json.loads(request.data)
    result_id = data.get('result_id')
    result = ReportService.create_report(result_id)
    return jsonify(result)


@report.route('/get_report', methods=['POST'])
def get_report():
    """获取报告内容"""
    data = json.loads(request.data)
    report_id = data.get('report_id')
    result = ReportService.get_report(report_id)
    report_path = None
    if result.get('code') == '0':
        report_path = result.get('report')

    if not report_path or not os.path.exists(report_path):
        return result

    return send_file(
        report_path,
        conditional=True,
        etag=True
    )

@report.route('/set_report', methods=['POST'])
def set_report():
    """修改报告"""
    data = json.loads(request.data)
    report_id = data.get('report_id')
    update_data = data.get('update_data')
    result = ReportService.set_report(report_id, update_data)
    return jsonify(result)


@report.route('/delete_report', methods=['POST'])
def delete_report():
    """删除报告"""
    data = json.loads(request.data)
    report_id = data.get('report_id')
    result = ReportService.delete_report(report_id)
    return jsonify(result)
