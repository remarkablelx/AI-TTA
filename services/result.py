from models.result import db, Result
from models.video import Video
from models.record import Record
from aimodel.algorithm_logic import ball_detect, pose_detect, action_split, action_detect
import os

class ResultService:
    @staticmethod
    def generate_result(record_id):
        """
        视频分析流水线,根据视频编号获取视频并进行分析，保存到数据库并返回分析结果
        :param record_id: 分析记录编号
        :return dict: 生成结果
        """
        #获取视频路径
        record = Record.query.get(record_id)
        record.state = 1
        video_id = record.video_id
        video_path = Video.query.get(video_id).video_path

        if not os.path.exists(video_path):
            print(f"错误: 初始输入视频不存在: {video_path}")
            exit(1)

        print("=" * 25 + " 开始执行端到端视频分析流水线 " + "=" * 25)

        # 创建一个主字典来收集所有路径
        pipeline_results = {'video_path': video_path}

        # --- 步骤 1: 球体轨迹跟踪 ---
        success, ball_result = ball_detect(video_path=video_path)
        if not success:
            print(f"流程终止于【球体跟踪】。错误: {ball_result.get('error')}")
            exit(1)

        pipeline_results.update(ball_result)
        print("步骤 1/4 完成。")

        # --- 步骤 2: 人体骨骼点检测 ---
        success, pose_result = pose_detect(video_path=pipeline_results["ball_video_out_path"])
        if not success:
            print(f"流程终止于【骨骼点检测】。错误: {pose_result.get('error')}")
            exit(1)

        pipeline_results.update(pose_result)
        print("步骤 2/4 完成。")

        # --- 步骤 3: 基于球轨迹的动作切分 ---
        success, segment_result = action_split(ball_json_path=pipeline_results["ball_json_out_path"])
        if not success:
            print(f"流程终止于【动作片段切分】。错误: {segment_result.get('error')}")
            exit(1)

        pipeline_results.update(segment_result)
        print("步骤 3/4 完成。")

        # --- 步骤 4: 动作识别与视频生成 ---
        success, final_result = action_detect(
            video_input_path=pipeline_results["pose_video_out_path"],
            pose_json_path=pipeline_results["pose_json_out_path"],
            segment_json_path=pipeline_results["segment_json_path"],
        )
        if not success:
            print(f"流程终止于【动作识别】。错误: {final_result.get('error')}")
            exit(1)

        pipeline_results.update(final_result)
        print("步骤 4/4 完成。")

        try:
            # 创建分析结果对象
            result = Result(
                video_id=video_id,
                ball_json_path=pipeline_results.get("ball_json_out_path", ""),
                pose_json_path=pipeline_results.get("pose_json_out_path", ""),
                ball_video_path=pipeline_results.get("ball_video_out_path", ""),
                pose_video_path=pipeline_results.get("pose_video_out_path", ""),
                segment_json_path=pipeline_results.get("segment_json_path", ""),
                annotated_video_path=pipeline_results.get("annotated_video_path", ""),
                recognition_json_path=pipeline_results.get("recognition_json_path", "")
            )

            record = Record.query.get(record_id)
            record.state = 2
            db.session.add(result)
            db.session.commit()

            # 添加结果ID到返回数据
            pipeline_results["result_id"] = result.result_id

        except Exception as e:
            db.session.rollback()
            return {"code": '-1','message':f"保存结果到数据库失败: {str(e)}"}

        # 返回完整的分析结果
        return {
            'code': 0,
            'message': '视频分析成功',
            'result':pipeline_results
        }


    @staticmethod
    def get_result(result_id):
        """获取分析结果详情
        :param result_id: 结果ID
        :return: 结果详情字典
        """
        result = Result.query.get(result_id)
        return {
            'code': 0,
            'message': '视频分析成功',
            'result': result.to_dict()
        }

    @staticmethod
    def set_result(result_id, update_data):
        """更新分析结果信息
        :param result_id: 结果ID
        :param update_data: 更新数据字典
        :return: 操作结果字典
        """
        try:
            result = Result.query.get(result_id)
            # 遍历更新字段
            for field, value in update_data.items():
                setattr(result, field, value)

            # 保存到数据库
            db.session.commit()

            return {
                'code': '1',
                'message': '分析结果更新成功',
                'updated_fields': { f"{field}": value for field, value in update_data.items() }
            }

        except Exception as e:
            db.session.rollback()
            return {
                'code': '-1',
                'message': f'分析结果更新失败: {str(e)}'
            }




