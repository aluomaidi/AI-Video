#视频翻译：抽音频->抽无声视频->音频识别（生成字幕）->字幕翻译->字幕合成音频-->合并音频和视频->合成字幕->添加水印
import asyncio
import os
import extractor as extractor
import recognizer as recognizer
import translator as translator
import synthesizer as synthesizer
from utils import sync_audio_video, sync_video_subtitle, extract_filename, get_media_length


original_video = "中国工厂.mp4"
original_language = 'zh'
trans_language = 'en'
voice = 'zh-CN-XiaoxiaoNeural'

app_id = "e8437c4a"
api_key = "35586b25a94f4b4fe61889fc307eaabf"
api_secret = "OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl"


output_dir = 'output'
filename, _ = extract_filename(original_video)
#original_audio = os.path.join(output_dir, f"{filename}.mp3")
#video_without_audio = os.path.join(output_dir, f"{filename}_without_audio.mp4")
original_srt = os.path.join(output_dir, f"{filename}.srt")
trans_srt = os.path.join(output_dir, f"{filename}_trans.srt")
trans_audio = os.path.join(output_dir, f"{filename}_trans_audio.mp3")
trans_video = os.path.join(output_dir, f"{filename}_{original_language}_to_{trans_language}.mp4")
trans_video_subtitle = os.path.join(output_dir, f"{filename}_{original_language}_to_{trans_language}_subtitle.mp4")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#抽音频
original_audio = extractor.extract_audio(original_video, output_dir)
#抽无声视频
video_without_audio = extractor.extract_video_without_audio(original_video, output_dir)
#音频识别（生成字幕）
_, srt_file = recognizer.speech_to_srt(original_audio, original_language, output_dir, "medium")
# 字幕翻译
trans_srt = translator.subtitle_translate(app_id, api_key, api_secret, srt_file, original_language, trans_language)
# 字幕合成音频
asyncio.run(synthesizer.srt_to_speech(trans_srt, trans_audio, voice))
# 合并音频和视频,并同步时长
sync_audio_video(video_without_audio, trans_audio, trans_video)
# 视频加字幕
sync_video_subtitle(trans_video, trans_srt, get_media_length(original_video), trans_video_subtitle)
#删除临时文件
os.remove(original_audio)
os.remove(video_without_audio)
os.remove(original_srt)
os.remove(trans_srt)
os.remove(trans_audio)