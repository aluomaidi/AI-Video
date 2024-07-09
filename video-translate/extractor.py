import ffmpeg
import subprocess
import shlex
import os
from execute_time import execute_time
from utils import extract_filename

@execute_time
def extract_audio(video, path="."):
    filename, _ = extract_filename(video)
    audio_name = path + "/" + filename + ".mka"
    cmd = f"ffmpeg -i {video} -vn -acodec copy {audio_name} -y"
    subprocess.run(shlex.split(cmd))
    return audio_name
    #ffmpeg.input(video).filter('highpass', '300').output(audio, format=audio_format).run(overwrite_output=True)

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
def extract_video_without_audio(video, path="."):
    filename, suffix = extract_filename(video)
    video_name = path + "/" + filename + "-noaudio" + suffix
    cmd = f"ffmpeg -i {video} -c:v copy -an {video_name} -y"
    subprocess.run(shlex.split(cmd))
    return video_name

if __name__ == '__main__':
    video = 'gzhmWuiE.mp4'
    audio = extract_audio(video, "output")
    video = extract_video_without_audio(video, "output")
