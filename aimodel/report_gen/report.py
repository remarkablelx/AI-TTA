import os
import json
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# 初始化与配置加载
def load_environment():
    # 加载环境变量并返回千帆 API Key
    current_path = os.path.dirname(os.path.abspath(__file__))
    parent_path = os.path.dirname(current_path)
    env_path = os.path.join(parent_path,'report_gen','.env')
    load_dotenv(env_path)
    api_key = os.getenv("QIANFAN_API_KEY")
    if not api_key:
        raise ValueError("错误: 未在 .env 文件中找到 QIANFAN_API_KEY。")
    return api_key


def load_skeleton_data(file_path: str):
    # 加载骨骼点数据
    print(f"正在从 {file_path} 加载骨骼点数据...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"错误: 输入文件不存在于路径 {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    instance_info = data.get('instance_info', [])
    meta_info = data.get('meta_info', {})

    if not instance_info:
        raise ValueError("错误: JSON 文件中未找到 'instance_info' 或其内容为空。")

    print("骨骼点数据加载成功。")
    return instance_info, meta_info


# 大模型交互与报告生成

def generate_report(input_json_path: str):
    try:
        api_key = load_environment()
        client = OpenAI(api_key=api_key, base_url="https://qianfan.baidubce.com/v2")
        skeleton_instances, meta_info = load_skeleton_data(input_json_path)

        per_frame_analyses = []
        batch_size = 10

        # 使用 ERNIE-Speed-8K 模型
        ANALYSIS_MODEL = "deepseek-r1"

        print(f"\n--- 开始第一阶段：逐批次分析帧数据 (使用模型: {ANALYSIS_MODEL}) ---")


        for i in range(0, len(skeleton_instances), batch_size):
            batch_instances = skeleton_instances[i: i + batch_size]

            prompt_stage1 = f"""
你是一个专业的乒乓球运动动作分析专家，擅长通过人体骨骼关键点坐标进行动作识别和姿态评估。请根据以下每帧图像中进行乒乓球对打时的人体骨骼点信息，结合字段说明，对前两个人的动作进行详细分析。分析内容应包括但不限于：

1. 动作是否规范；
2. 姿态是否稳定，是否存在不协调或危险的动作；
3. 动作幅度是否合理；
4. 如存在问题，请指出具体关键点及改进建议。

只为前两个人体进行分析，并且考虑到当前图像帧的编号，便于最后根据整体的运动轨迹进行分析。
输出标签使用：人体1、人体2
以下是骨骼点字段说明（metadata）：
{meta_info}

以下是第 {i + 1} 到 {min(i + batch_size, len(skeleton_instances))} 帧图像中的每个人体的骨骼点数据：
"""
            for j, skeleton_instance in enumerate(batch_instances):
                prompt_stage1 += f"\n第 {i + j + 1} 帧图像中的每个人体的骨骼点数据：\n{skeleton_instance}"

            print(f"正在分析第 {i + 1}-{min(i + batch_size, len(skeleton_instances))} 帧...")

            completion = client.chat.completions.create(
                model=ANALYSIS_MODEL,
                messages=[
                    {"role": "system", "content": "你是乒乓球运动动作分析专家"},
                    {"role": "user", "content": prompt_stage1},
                ],
                stream=False,
            )
            per_frame_analyses.append(completion.choices[0].message.content)

            time.sleep(1)

        print("--- 第一阶段分析完成 ---")

        print(f"\n--- 开始第二阶段：生成综合分析报告 (使用模型: {ANALYSIS_MODEL}) ---")

        prompt_final = f"""
你是一个专业的乒乓球运动动作分析专家，请根据以下每一帧的分析结果，对每个人的乒乓球动作进行独立分析并撰写报告。报告应包括但不限于以下内容：

1. **动作规范性评价**：该人的动作是否符合标准乒乓球动作要求。包括站位、击球动作、挥拍角度等是否标准。
2. **危险/异常动作**：是否存在不协调或危险的动作（例如：过度伸展、非正常的身体姿势等）。
3. **动作连贯性和节奏**：该人动作是否流畅，是否有停顿或节奏问题，动作的起始和结束是否平衡。
4. **改进建议**：如果动作中存在问题，请根据每一帧中的骨骼点分析给出改进的具体建议。
5. **综合评价**：结合整体运动表现，给出该人运动表现的总体评价。

### 以下是每一帧的分析内容，基于骨骼点数据和动作分析：
{per_frame_analyses}

请为每个的运动员生成详细的报告，每个人的分析按以下格式输出：
- **运动员1**:
    - 动作规范性评价：
    - 危险/异常动作：
    - 动作连贯性和节奏：
    - 改进建议：
    - 综合评价：
- **运动员2**:
    - 动作规范性评价：
    - 危险/异常动作：
    - 动作连贯性和节奏：
    - 改进建议：
    - 综合评价：

请确保每个运动员的动作分析清晰且详细，最终输出每个运动员的综合表现和改进建议。
"""

        response = client.chat.completions.create(
            model=ANALYSIS_MODEL,
            messages=[
                {"role": "system", "content": "你是乒乓球运动动作分析专家"},
                {"role": "user", "content": prompt_final},
            ],
            stream=False,
        )
        final_report = response.choices[0].message.content
        print("--- 第二阶段分析完成，报告已生成 ---")

        # 保存报告
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_path = os.path.dirname(current_path)
        output_dir = os.path.join(parent_path, 'report')
        os.makedirs(output_dir, exist_ok=True)

        input_basename = os.path.splitext(os.path.basename(input_json_path))[0]
        output_report_path = os.path.join(output_dir, f"{input_basename}_report.md")

        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write(final_report)

        print(f"\n分析报告已成功保存至: {os.path.abspath(output_report_path)}")

        return final_report, os.path.abspath(output_report_path)

    except Exception as e:
        print(f"程序执行出错: {e}")
        return None, None


if __name__ == '__main__':
    generate_report("../json/tt_ball_detect_pose_detect.json")