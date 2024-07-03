#视频翻译：抽音频->抽帧->音频识别（生成字幕）->字幕翻译->字幕合成音频->合成图片帧为视频->合并音频和视频->合成字幕-》添加水印
import asyncio
import subprocess
import os
import extractor as extractor
import recognizer as recognizer
import translator as translator
import synthesizer as synthesizer

original_video = "数字人播报.mp4"
original_language = 'zh'
original_audio = 'output/origin_audio.mp3'
original_srt = 'output/origin_audio.srt'
trans_language = 'en'
trans_video = "output/数字人播报_en.mp4"
trans_audio = "output/trans.mp3"
trans_srt = "output/trans.srt"
fps = '30'
frames_pattern = 'frame_%06d.png'
frames_dir = 'output/frames/'
voice = 'zh-CN-XiaoxiaoNeural'

app_id = "e8437c4a"
api_key = "35586b25a94f4b4fe61889fc307eaabf"
api_secret = "OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl"

if not os.path.exists("output"):
    os.makedirs("output")
    
#抽音频
extractor.extract_audio(original_video, original_audio)
#抽帧
extractor.extract_frames(original_video, frames_dir, fps, frames_pattern)
#音频识别（生成字幕）
recognizer.speech_to_srt(original_audio, original_language, 'output')
# 字幕翻译
translator.subtitle_translate(app_id, api_key, api_secret, original_srt, trans_srt, original_language, trans_language)
# 字幕合成音频
asyncio.run(synthesizer.srt_to_speech(trans_srt, trans_audio, voice))

# 合成图片帧为视频
subprocess.run([
    'ffmpeg', '-framerate', fps, '-i', frames_dir + frames_pattern,
    '-c:v', 'libx264', '-r', fps, '-pix_fmt', 'yuv420p', 'output/frames_video.mp4', '-y'
])

# 合并音频和视频
subprocess.run([
    'ffmpeg', '-i', 'output/frames_video.mp4', '-i', trans_audio,
    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', 'output/video_with_audio.mp4', '-y'
])

# 合成字幕
subprocess.run([
    'ffmpeg', '-i', 'output/video_with_audio.mp4', '-vf', f'subtitles={trans_srt}',
    '-c:a', 'copy', trans_video, '-y'
])