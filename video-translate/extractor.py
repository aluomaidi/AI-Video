import ffmpeg
import subprocess
import shlex
import os
from execute_time import execute_time

@execute_time
def extract_audio(video, audio, audio_format='mp3'):
    ffmpeg.input(video).filter('highpass', '300').output(audio, format=audio_format).run(overwrite_output=True)

@execute_time
def extract_frames(video, frames_dir, fps='24', frames_pattern='frame_%06d.png'):
    # 如果目录不存在，则创建它
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    # 输出文件的模式，指定目录和文件名模式
    output_pattern = os.path.join(frames_dir, frames_pattern)
    # 调用 ffmpeg 抽帧
    subprocess.run(['ffmpeg', '-i', video, '-vf', f'fps={fps}', output_pattern, '-y'])

@execute_time
def extract_video_without_audio(input_video, output_video):
    """
    从视频文件中提取无声视频。
    
    参数:
    input_video (str): 输入视频文件的路径。
    output_video (str): 输出无声视频文件的路径。
    """
    cmd = f"ffmpeg -i {input_video} -an {output_video} -y"
    subprocess.run(shlex.split(cmd))

if __name__ == '__main__':
    video = '重庆森林片段.mp4'
    audio = 'output/重庆森林片段.mp3'
    extract_audio(video, audio) 

    extract_frames(video, "output/frames")