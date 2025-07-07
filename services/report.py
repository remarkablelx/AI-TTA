from models.report import db, Report
from models.result import Result
from aimodel.report_gen.report import generate_report

class ReportService:
    @staticmethod
    def create_report(result_id):
        """调用报告生成器创建报告"""
        try:
            result = Result.query.get(result_id)
            # 调用报告生成函数
            report_content, report_path = generate_report(result.pose_json_path)

            # 创建报告记录
            new_report = Report(
                pose_estimate=report_path,
                result_id=result_id,
            )
            db.session.add(new_report)
            db.session.commit()

            return {
                'code':'0',
                'message':'报告生成成功',
                'report':new_report.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code':'-1',
                'message':f'报告生成失败{str(e)}'
            }

    @staticmethod
    def get_report(report_id: int):
        """获取单个报告"""
        report = Report.query.get(report_id)
        if not report:
            return {
                'code':'-1',
                'message':f'报告不存在'
            }
        return {
            'code':'0',
            'message':'报告获取成功',
            'report':report.pose_estimate
        }

    @staticmethod
    def set_report(report_id: int, data: str):
        """修改报告内容"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return {
                    'code':'-1',
                    'message':f'报告不存在'
                }
            report.pose_estimate = data

            db.session.commit()
            return {
                'code':'0',
                'message':'报告更新成功',
                'report':report.to_dict()
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code':'-1',
                'message':f'报告更新失败{str(e)}'
            }


    @staticmethod
    def delete_report(report_id: int):
        """删除报告"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return {
                    'code':'-1',
                    'message':f'报告不存在'
                }

            db.session.delete(report)
            db.session.commit()

            return {
                'code':'0',
                'message':'报告删除成功',
                'report_id':report_id
            }
        except Exception as e:
            db.session.rollback()
            return {
                'code':'-1',
                'message':f'报告删除失败{str(e)}'
            }

