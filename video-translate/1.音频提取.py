import ffmpeg

input_file = '重庆森林片段.mp4'

audio_file = 'output/重庆森林片段.mp3'

# 使用音频滤波器提取人声
ffmpeg.input(input_file).filter('highpass', '300').output(audio_file, format='mp3', audio_bitrate='64k').run(overwrite_output=True)