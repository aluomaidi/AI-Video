import subprocess

final_video ="output/final_video.mp4"
frames = "output/frames/frame_%06d.png"
audio = "output/重庆森林片段.mp3"
subtitles = "output/重庆森林片段.srt"
# 水印文字和位置
watermarks = [
    {'text': '羚羊', 'x': '40', 'y': '40'},        # 左上角
    {'text': '羚羊', 'x': 'w-tw-40', 'y': '40'},   # 右上角
    {'text': '羚羊', 'x': '40', 'y': 'h-th-40'},   # 左下角
    {'text': '羚羊', 'x': 'w-tw-40', 'y': 'h-th-40'} # 右下角
]

# 构建 drawtext 滤镜字符串
drawtext_filters = ','.join(
    [f"drawtext=text='{wm['text']}':fontcolor=white:fontsize=24:x={wm['x']}:y={wm['y']}" for wm in watermarks]
)

# 合成图片帧为视频
subprocess.run([
    'ffmpeg', '-framerate', '24', '-i', frames,
    '-c:v', 'libx264', '-r', '24', '-pix_fmt', 'yuv420p', 'output/frames_video.mp4', '-y'
])

# 合并音频和视频
subprocess.run([
    'ffmpeg', '-i', 'output/frames_video.mp4', '-i', audio,
    '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', 'output/video_with_audio.mp4', '-y'
])

# 合并字幕
subprocess.run([
    'ffmpeg', '-i', 'output/video_with_audio.mp4', '-vf', f'subtitles={subtitles}',
    '-c:a', 'copy', 'output/video_with_subtitle.mp4', '-y'
])

# 添加多个文字水印
subprocess.run([
    'ffmpeg', '-i', 'output/video_with_subtitle.mp4',
    '-vf', drawtext_filters,
    '-c:a', 'copy', final_video, '-y'
])