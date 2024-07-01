import subprocess

# 提取视频中的音频
input_file = '重庆森林片段.mp4'
audio_file = 'audio.wav'
subprocess.run(['ffmpeg', '-i', input_file, audio_file, '-y'])

# 使用 Demucs 分离音频
subprocess.run(['demucs', audio_file])

print("音频分离完成，结果保存在 'separated' 目录中")
