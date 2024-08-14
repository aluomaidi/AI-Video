import asyncio
import edge_tts
import os
import subprocess
from utils import parse_srt_file
from execute_time import execute_time
import shlex

def merge_audio_clips_with_timestamps(srt_data, temp_files, audio_file):
    # 提取时间戳信息
    timestamps = [timestamp for timestamp, _ in srt_data]
    # 构建ffmpeg命令
    ffmpeg_command = [
        "ffmpeg",
        "-i", "concat:" + "|".join(temp_files),  # 指定要合并的文件列表
        "-c", "copy",  # 使用copy模式进行合并，不重新编码
        "-metadata:s:a:0", f"start_time={timestamps[0]}",  # 设置合并后的音频起始时间
        audio_file, "-y"
    ]

    # 执行ffmpeg命令
    subprocess.run(ffmpeg_command, check=True)
    
@execute_time    
async def text_to_speech(text, audio_file, voice, rate='+0%'):
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(audio_file)
    except Exception as e:
        print(f"An error occurred during synthesis: {e}")

@execute_time
async def srt_to_speech(srt, audio_file, voice, rate='+0%'):
    srt_data = parse_srt_file(srt)
    temp_files = []
    #提取整个视频的起始时间，应对某些视频开始不说话的场景
    timestamp = srt_data[0][0]
    start, _ = timestamp.split(" --> ")
    # 处理开始时间
    start_parts = start.split(":")
    start_hours = int(start_parts[0])
    start_minutes = int(start_parts[1])
    start_seconds, start_milliseconds = map(int, start_parts[2].replace(",", ".").split("."))
    # 计算新的开始时间（以毫秒为单位）
    start_time_miliseconds = (start_hours * 3600 + start_minutes * 60 + start_seconds) * 1000 + start_milliseconds
   
    # 生成音频文件
    for index, (_, text) in enumerate(srt_data):
        temp_file = f"temp_{index}.mp3"
        temp_files.append(temp_file)
        task = asyncio.create_task(text_to_speech(text, temp_file, voice, rate))
        await task

    merge_audio_clips_with_timestamps(srt_data, temp_files, audio_file)
    # 清理临时文件
    for temp_file in temp_files:
        os.remove(temp_file)

    return start_time_miliseconds    

if __name__ == "__main__":
    # Example usage
    # text = '''陕西，这片古老而神秘的土地，不仅有着悠久的历史文化，更蕴藏着丰富的特产资源。今天，我要给大家介绍几款陕西的特色美食，让你在品味中感受陕西的独特魅力。
    #     首先，我们要说的是那色香味俱佳的陕西凉皮。选用优质小麦粉，经过独特的工艺制成，口感滑爽，搭配秘制酱料，酸辣适中，让人回味无穷。无论是炎炎夏日还是寒冷冬季，一碗凉皮都能带给你不一样的味觉享受。
    #     接下来，是让人垂涎三尺的肉夹馍。选用上等猪肉，经过慢火炖煮，肉质酥软，香气四溢。搭配手工制作的白面馍，外酥里嫩，每一口都是满满的幸福感。无论是早餐还是下午茶，肉夹馍都是你不二的选择。
    #     最后，我们要推荐的是陕西的特色零食——柿饼。选用新鲜柿子，经过晾晒、腌制等多道工序制成，甜而不腻，营养丰富。无论是自己品尝还是送给亲朋好友，柿饼都是一份充满心意的礼物。
    #     现在购买还有优惠活动哦！陕西凉皮、肉夹馍、柿饼，每一款都是地道的陕西风味，让你在品尝美食的同时，也能感受到陕西的热情与淳朴。快来选购吧，让这些美食为你的味蕾带来一场难忘的旅行！'''
    # audio = "output/synthesize.mp3"
    # voice = 'zh-CN-shaanxi-XiaoniNeural'
    # asyncio.run(text_to_speech(text, audio, voice))

    srt_file = "output/重庆森林片段_en.srt"
    audio_file = "output/synthesize.mp3"
    voice = 'zh-CN-XiaoxiaoNeural'
    asyncio.run(srt_to_speech(srt_file, audio_file, voice))
         

