#视频翻译：抽音频->抽无声视频->音频识别（生成字幕）->字幕翻译->字幕合成音频-->合并音频和视频->合成字幕->添加水印
import asyncio
import os
import extractor as extractor
import recognizer as recognizer
import translator as translator
import synthesizer as synthesizer
from utils import sync_audio_video, sync_video_subtitle, extract_filename, get_media_length


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
trans_video = os.path.join(output_dir, f"{filename}_{original_language}_to_{trans_language}.mp4")
trans_video_subtitle = os.path.join(output_dir, f"{filename}_{original_language}_to_{trans_language}_subtitle.mp4")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#抽音频
extractor.extract_audio(original_video, original_audio)
#抽无声视频
extractor.extract_video_without_audio(original_video, video_without_audio)
# 识别
text = recognizer.speech_to_text(original_audio, original_language)
# 翻译
trans_text = translator.text_translate(app_id, api_key, api_secret, text, original_language, trans_language)
# 合成
asyncio.run(synthesizer.text_to_speech(trans_text, trans_audio, voice))
# 合并音频和视频,并同步时长
sync_audio_video(video_without_audio, trans_audio, trans_video)

#删除临时文件
os.remove(original_audio)
os.remove(video_without_audio)
os.remove(trans_audio)