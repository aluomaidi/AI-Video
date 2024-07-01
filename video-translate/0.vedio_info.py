import ffmpeg

def get_video_audio_info(input_file):
    # 使用 ffmpeg.probe 获取视频信息
    probe = ffmpeg.probe(input_file)
    
    # 提取视频流信息
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream:
        video_info = {
            'nb_frames': video_stream.get('nb_frames', 'unknown'),
            'frame_rate': video_stream.get('r_frame_rate', 'unknown'),
            'codec_name': video_stream.get('codec_name', 'unknown'),
            'width': video_stream.get('width', 'unknown'),
            'height': video_stream.get('height', 'unknown'),
            'duration': video_stream.get('duration', 'unknown'),
            'bit_rate': video_stream.get('bit_rate', 'unknown'),
            'pix_fmt': video_stream.get('pix_fmt', 'unknown'),
            'sample_aspect_ratio': video_stream.get('sample_aspect_ratio', 'unknown'),
            'display_aspect_ratio': video_stream.get('display_aspect_ratio', 'unknown'),
            'tags': video_stream.get('tags', {})
        }
    else:
        video_info = {}
    
    # 提取音频流信息
    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    if audio_stream:
        audio_info = {
            'codec_name': audio_stream.get('codec_name', 'unknown'),
            'sample_rate': audio_stream.get('sample_rate', 'unknown'),
            'channels': audio_stream.get('channels', 'unknown'),
            'bit_rate': audio_stream.get('bit_rate', 'unknown'),
            'tags': audio_stream.get('tags', {})
        }
    else:
        audio_info = {}

    return video_info, audio_info


input_file = '重庆森林片段.mp4'

video_info, audio_info = get_video_audio_info(input_file)

print('视频信息:')
for key, value in video_info.items():
    print(f'{key}: {value}')

print('\n音频信息:')
for key, value in audio_info.items():
    print(f'{key}: {value}')

output_subtitle_file = 'output_subtitles.srt'