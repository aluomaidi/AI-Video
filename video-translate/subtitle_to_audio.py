import asyncio
import edge_tts
import os
import subprocess

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

async def synthesize_text_to_audio(text, output_file, voice='en-US-AriaNeural'):
    """
    合成文本为音频并保存到文件。
    Args:
        text (str): 要合成的文本。
        output_file (str): 输出音频文件的路径。
        voice (str): 使用的语音。
    """
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        print(f"Audio content written to file {output_file}")
    except Exception as e:
        print(f"An error occurred during synthesis: {e}")

def merge_audio_clips_with_timestamps(srt_data, temp_files, output_file):
    """
    使用ffmpeg合并多个音频文件为一个音频文件，根据字幕文件中的时间戳信息。
    Args:
        srt_data (List[Tuple[str, str]]): 包含时间戳和文本的列表。
        temp_files (List[str]): 需要合并的音频文件路径列表。
        output_file (str): 输出合并后的音频文件路径。
    """
    # 提取时间戳信息
    timestamps = [timestamp for timestamp, _ in srt_data]

    # 构建ffmpeg命令
    ffmpeg_command = [
        "ffmpeg",
        "-i", "concat:" + "|".join(temp_files),  # 指定要合并的文件列表
        "-c", "copy",  # 使用copy模式进行合并，不重新编码
        "-metadata:s:a:0", f"start_time={timestamps[0]}",  # 设置合并后的音频起始时间
        output_file, "-y"
    ]

    # 执行ffmpeg命令
    subprocess.run(ffmpeg_command, check=True)

async def main(srt_file, output_file, voice='en-US-AriaNeural'):
    srt_data = parse_srt_file(srt_file)
    temp_files = []

    for index, (timestamp, text) in enumerate(srt_data):
        temp_file = f"temp_{index}.mp3"
        temp_files.append(temp_file)
        await synthesize_text_to_audio(text, temp_file, voice)

    merge_audio_clips_with_timestamps(srt_data, temp_files, output_file)

    # 清理临时文件
    for temp_file in temp_files:
        os.remove(temp_file)

if __name__ == "__main__":
    srt_file = "output/重庆森林片段.srt"
    output_file = "output/synthesize.mp3"
    # voice = 'zh-CN-shaanxi-XiaoniNeural'
    voice = 'zh-CN-XiaoxiaoNeural'

    asyncio.run(main(srt_file, output_file, voice))