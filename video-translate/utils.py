
from typing import List, Tuple
import subprocess
import shlex
import os

def parse_srt_file(srt_file):
    """
    解析 SRT 字幕文件，返回一个包含时间戳和文本的列表。
    Args:
        srt_file (str): SRT 字幕文件的路径。
    Returns:
        List[Tuple[str, str]]: 一个包含时间戳和文本的列表。
    """
    with open(srt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    entries = []
    entry = []
    for line in lines:
        line = line.strip()
        if not line:
            if entry:
                entries.append(entry)
                entry = []
        else:
            entry.append(line)

    # 处理最后一个条目（如果有）
    if entry:
        entries.append(entry)

    # 提取时间戳和文本
    srt_data = []
    for entry in entries:
        if len(entry) >= 3:
            # 时间戳在第二行，格式如：00:00:10,500 --> 00:00:13,000
            timestamp = entry[1]
            # 文本在第三行及以后
            text = ' '.join(entry[2:])
            srt_data.append((timestamp, text))

    return srt_data

def save_srt_file(srt_data: List[Tuple[str, str]], output_file: str):
    """
    将包含时间戳和文本的列表存储到 SRT 字幕文件中。

    Args:
        srt_data (List[Tuple[str, str]]): 一个包含时间戳和文本的列表。
        output_file (str): 输出 SRT 文件的路径。
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, (timestamp, text) in enumerate(srt_data, start=1):
            file.write(f"{index}\n")
            file.write(f"{timestamp}\n")
            file.write(f"{text}\n\n")
 #提取文件名称的函数
def extract_filename(file_path):
    base_name = os.path.basename(file_path)
    filename, _ = os.path.splitext(base_name)  # 分割文件名和扩展名
    return base_name, filename


def get_media_length(file_path):
    """
    获取媒体文件的长度（以秒为单位）。
    """
    cmd = f"ffprobe -v error -show_entries format=duration -of csv=p=0 {file_path}"
    result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return float(result.stdout.strip())

def adjust_audio_speed(input_audio, adjustment_ratio, output_audio):
    """
    调整音频速度。adjustment_ratio: 调整速率的比例。例如，0.5 表示播放速度减慢一半，2.0 表示播放速度加快一倍
    """
    cmd = f"ffmpeg -i {input_audio} -filter:a 'atempo={adjustment_ratio}' -vn {output_audio} -y"
    subprocess.run(shlex.split(cmd))

def adjust_video_speed(input_video, adjustment_ratio, output_video):
    """
    调整视频速度。adjustment_ratio: 调整速率的比例。例如，0.5 表示播放速度减慢一半，2.0 表示播放速度加快一倍。
    """
    cmd = f"ffmpeg -i {input_video} -filter:v 'setpts={1/adjustment_ratio}*PTS' {output_video} -y"
    subprocess.run(shlex.split(cmd))

def merge_audio_video(input_video, input_audio, output_file):
    """
    合并音频和视频文件。
    """
    cmd = f"ffmpeg -i {input_video} -i {input_audio} -c:v copy -c:a aac {output_file} -y"
    subprocess.run(shlex.split(cmd))

def sync_audio_video(input_video, input_audio, output_final, threshold=1.35):
    # 获取视频和音频长度
    video_length = get_media_length(input_video)
    audio_length = get_media_length(input_audio)
    print(f"Video length: {video_length} seconds")
    print(f"Audio length: {audio_length} seconds")

    # 音视频长度差异比例
    ratio = 1
    adjusted_audio = "adjusted_audio.mp3"
    adjusted_video = "adjusted_video.mp4"

    if audio_length > video_length: #音频加速，视频减速
        ratio = audio_length / video_length
        if ratio < threshold:
            print("Adjusting audio speed to match video speed.")
            adjust_audio_speed(input_audio, ratio, adjusted_audio)
            merge_audio_video(input_video, adjusted_audio, output_final)
        elif ratio < threshold * threshold:
            print("Audio speed adjustment exceeds threshold.  Adjusting both.")
            adjust_audio_speed(input_audio, threshold, adjusted_audio)
            adjust_video_speed(input_video, threshold/ratio, adjusted_video)
            merge_audio_video(adjusted_video, adjusted_audio, output_final)
        else:
            print("Audio speed adjustment exceeds threshold. Skipping.")
    else: #视频加速、音频减速
        ratio = video_length / audio_length
        if ratio < threshold:
            print("Adjusting video speed to match audio speed.")
            adjust_video_speed(input_video, ratio, adjusted_video)
            merge_audio_video(adjusted_video, input_audio, output_final)
        elif ratio < threshold * threshold:
            print("Video speed adjustment exceeds threshold. Adjusting both.")
            adjust_audio_speed(input_audio, 1/threshold, adjusted_audio)
            adjust_video_speed(input_video, ratio/threshold, adjusted_video)
            merge_audio_video(adjusted_video, adjusted_audio, output_final)
        else:
            print("Video speed adjustment exceeds threshold. Skipping.")    

    # 删除临时文件
    subprocess.run(shlex.split(f"rm {adjusted_audio} {adjusted_video}"))

def split_video(input_video, start_time, duration, output_video):
    """
    拆分视频文件。
    
    参数:
    input_video (str): 输入视频文件的路径。
    start_time (str): 开始时间，格式为 "HH:MM:SS"。
    duration (str): 持续时间，格式为 "HH:MM:SS"。
    output_video (str): 输出视频文件的路径。
    """
    cmd = f"ffmpeg -i {input_video} -ss {start_time} -t {duration} -c copy {output_video} -y"
    subprocess.run(shlex.split(cmd))
    
if __name__ == "__main__":
    input_video = "output/frames_video.mp4"
    input_audio = "output/trans.mp3"
    output_final = "output_final.mp4"
    threshold = 1.35
    sync_audio_video(input_video, input_audio, output_final, threshold)            