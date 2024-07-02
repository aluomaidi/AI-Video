
from typing import List, Tuple

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