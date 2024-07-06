
from typing import List, Tuple
import subprocess
import shlex
import os
import math
from execute_time import execute_time

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

def multiply_timestamp(timestamp, multiplier):
    # 将时间戳拆分成开始时间和结束时间部分
    start, end = timestamp.split(" --> ")

    # 处理开始时间
    start_parts = start.split(":")
    start_hours = int(start_parts[0])
    start_minutes = int(start_parts[1])
    start_seconds, start_milliseconds = map(int, start_parts[2].replace(",", ".").split("."))

    # 计算新的开始时间（以秒为单位）
    total_start_seconds = (start_hours * 3600 + start_minutes * 60 + start_seconds) * multiplier
    total_start_seconds += start_milliseconds * multiplier / 1000

    # 转换回小时、分钟、秒和毫秒
    new_start_hours = int(total_start_seconds // 3600)
    total_start_seconds %= 3600
    new_start_minutes = int(total_start_seconds // 60)
    total_start_seconds %= 60
    new_start_seconds = int(total_start_seconds)
    new_start_milliseconds = int((total_start_seconds - new_start_seconds) * 1000)

    # 格式化新的开始时间
    new_start_time = "{:02}:{:02}:{:02},{:03}".format(
        new_start_hours, new_start_minutes, new_start_seconds, new_start_milliseconds
    )

    # 处理结束时间
    end_parts = end.split(":")
    end_hours = int(end_parts[0])
    end_minutes = int(end_parts[1])
    end_seconds, end_milliseconds = map(int, end_parts[2].replace(",", ".").split("."))

    # 计算新的结束时间（以秒为单位）
    total_end_seconds = (end_hours * 3600 + end_minutes * 60 + end_seconds) * multiplier
    total_end_seconds += end_milliseconds * multiplier / 1000

    # 转换回小时、分钟、秒和毫秒
    new_end_hours = int(total_end_seconds // 3600)
    total_end_seconds %= 3600
    new_end_minutes = int(total_end_seconds // 60)
    total_end_seconds %= 60
    new_end_seconds = int(total_end_seconds)
    new_end_milliseconds = int((total_end_seconds - new_end_seconds) * 1000)

    # 格式化新的结束时间
    new_end_time = "{:02}:{:02}:{:02},{:03}".format(
        new_end_hours, new_end_minutes, new_end_seconds, new_end_milliseconds
    )

    # 返回新的时间戳字符串
    return f"{new_start_time} --> {new_end_time}"

def adjust_subtitle_timestamp(subtitle, multiplier):
    srt_data = parse_srt_file(subtitle)
    new_srt_data = []
    for index, (timestamp, text) in enumerate(srt_data):
        new_timestamp = multiply_timestamp(timestamp, multiplier)
        new_srt_data.append((new_timestamp, text))  
    subtitle = "output.srt"    
    save_srt_file(new_srt_data, subtitle)
    return subtitle            
 #提取文件名称的函数
def extract_filename(file_path):
    base_name = os.path.basename(file_path)
    return os.path.splitext(base_name)

def get_media_length(file_path):
    """
    获取媒体文件的长度（以秒为单位）。
    """
    cmd = f"ffprobe -v error -show_entries format=duration -of csv=p=0 {file_path}"
    result = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return float(result.stdout.strip())

@execute_time
def adjust_audio_speed(input_audio, adjustment_ratio, output_audio):
    """
    调整音频速度。adjustment_ratio: 调整速率的比例。例如，0.5 表示播放速度减慢一半，2.0 表示播放速度加快一倍
    """
    cmd = f"ffmpeg -i {input_audio} -filter:a 'atempo={adjustment_ratio}' -vn {output_audio} -y"
    subprocess.run(shlex.split(cmd))

@execute_time
def adjust_video_speed(input_video, adjustment_ratio, output_video):
    """
    调整视频速度。adjustment_ratio: 调整速率的比例。例如，0.5 表示播放速度减慢一半，2.0 表示播放速度加快一倍。
    """
    cmd = f"ffmpeg -i {input_video} -filter:v 'setpts={1/adjustment_ratio}*PTS' -an {output_video} -y"
    subprocess.run(shlex.split(cmd))

def merge_audio_video(input_video, input_audio, output_file):
    cmd = f"ffmpeg -i {input_video} -i {input_audio} -c:v copy -c:a aac {output_file} -y"
    subprocess.run(shlex.split(cmd))

def merge_video_with_subtitle(input_video, subtitle_file, output_file):
    # FFmpeg命令，视频加字幕
    cmd = f"ffmpeg -i {input_video} -vf subtitles={subtitle_file} {output_file} -y"
    # 使用subprocess运行命令
    subprocess.run(shlex.split(cmd))

@execute_time
def sync_audio_video(input_video, input_audio, output_final):
    # 获取视频和音频长度
    video_length = get_media_length(input_video)
    audio_length = get_media_length(input_audio)
    adjusted_audio = "adjusted_audio.mp3"
    adjusted_video = "adjusted_video.mp4"
    #对齐音频和视频长度
    average = (audio_length + video_length) / 2
    adjust_audio_speed(input_audio, audio_length/average, adjusted_audio)
    adjust_video_speed(input_video, video_length/average, adjusted_video)
    merge_audio_video(adjusted_video, adjusted_audio, output_final)
    # 删除临时文件
    subprocess.run(shlex.split(f"rm {adjusted_audio} {adjusted_video}"))    

@execute_time
def sync_video_subtitle(input_video, subtitle, subtitle_length, output_final):
    # 获取视频长度
    video_length = get_media_length(input_video)
    #改字幕timestamp，确保字幕匹配视频
    subtitle_adjusted = adjust_subtitle_timestamp(subtitle, video_length/subtitle_length)
    merge_video_with_subtitle(input_video, subtitle_adjusted, output_final)
    # 删除临时文件
    subprocess.run(shlex.split(f"rm {subtitle_adjusted}"))

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

if __name__ == '__main__':
    # audio1 = 'output/gzhmWuiE.mka'
    # audio2 = 'output/gzhmWuiE_2.mka'

    # adjust_audio_speed(audio1, 1.5, audio2)

    video1 = 'output/gzhmWuiE-noaudio.mp4'
    video2 = 'output/gzhmWuiE-noaudio_2.mp4'

    adjust_video_speed(video1, 0.9, video2)