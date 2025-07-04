from models.result import db, Result
from models.video import Video

class ResultService:
    @staticmethod
    def generate_result(video_id):
        video = Video.query.get(video_id)
        #result = (video.video_path)

        return

    @staticmethod
    def get_result(result_id):
        result = Result.query.get(result_id)
        return result.to_dict()

    @staticmethod
    def set_result(result_id):
        return
