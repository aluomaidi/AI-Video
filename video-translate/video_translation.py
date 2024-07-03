#视频翻译：抽音频->抽帧->音频识别（生成字幕）->字幕翻译->字幕合成音频->合成图片帧为视频->合并音频和视频->合成字幕-》添加水印
import asyncio
import subprocess
import os
import extractor as extractor
import recognizer as recognizer
import translator as translator
import synthesizer as synthesizer
from utils import sync_audio_video, extract_filename


original_video = "数字人播报.mp4"
original_language = 'zh'
trans_language = 'en'
voice = 'zh-CN-XiaoxiaoNeural'

app_id = "e8437c4a"
api_key = "35586b25a94f4b4fe61889fc307eaabf"
api_secret = "OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl"


output_dir = 'output'
_, filename = extract_filename(original_video)
original_audio = os.path.join(output_dir, f"{filename}.mp3")
video_without_audio = os.path.join(output_dir, f"{filename}_without_audio.mp4")
original_srt = os.path.join(output_dir, f"{filename}.srt")
trans_srt = os.path.join(output_dir, f"{filename}_trans.srt")
trans_audio = os.path.join(output_dir, f"{filename}_trans_audio.mp3")
trans_video_without_subtitle = os.path.join(output_dir, f"{filename}_without_subtitle.mp4")
trans_video = os.path.join(output_dir, f"{filename}_{original_language}_to_{trans_language}.mp4")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#抽音频
extractor.extract_audio(original_video, original_audio)
#抽无声视频
extractor.extract_video_without_audio(original_video, video_without_audio)
#音频识别（生成字幕）
recognizer.speech_to_srt(original_audio, original_language, output_dir)
# 字幕翻译
translator.subtitle_translate(app_id, api_key, api_secret, original_srt, trans_srt, original_language, trans_language)
# 字幕合成音频
asyncio.run(synthesizer.srt_to_speech(trans_srt, trans_audio, voice))
# 合并音频和视频,并同步时长
sync_audio_video(video_without_audio, trans_audio, trans_video_without_subtitle)
# 合成字幕
subprocess.run([
    'ffmpeg', '-i', trans_video_without_subtitle, '-vf', f'subtitles={trans_srt}',
    '-c:a', 'copy', trans_video, '-y'
])
#删除临时文件
# os.remove(original_audio)
# os.remove(video_without_audio)
# os.remove(original_srt)
# os.remove(trans_srt)
# os.remove(trans_audio)
