import subprocess
import os

input_file = '重庆森林片段.mp4'
output_directory = 'output/frames'
output_pattern = 'frame_%06d.png'

# 如果目录不存在，则创建它
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 输出文件的模式，指定目录和文件名模式
output_pattern = os.path.join(output_directory, output_pattern)

# 调用 ffmpeg 抽帧
result = subprocess.run(['ffmpeg', '-i', input_file, '-vf', 'fps=24', output_pattern, '-y'])

# 检查命令执行是否成功
if result.returncode == 0:
    print("抽帧成功")
else:
    print("抽帧失败")
    print(result.stderr)
