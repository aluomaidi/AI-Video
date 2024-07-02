import ffmpeg
import subprocess
import os

def extract_audio(video, audio, audio_format='mp3'):
    ffmpeg.input(video).filter('highpass', '300').output(audio, format=audio_format).run(overwrite_output=True)

def extract_frames(video, frames_dir, fps='24', frames_pattern='frame_%06d.png'):
    # 如果目录不存在，则创建它
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    # 输出文件的模式，指定目录和文件名模式
    output_pattern = os.path.join(frames_dir, frames_pattern)
    # 调用 ffmpeg 抽帧
    subprocess.run(['ffmpeg', '-i', video, '-vf', f'fps={fps}', output_pattern, '-y'])
    
if __name__ == '__main__':
    video = '重庆森林片段.mp4'
    audio = 'output/重庆森林片段.mp3'
    extract_audio(video, audio) 

    extract_frames(video, "output/frames")