import subprocess
import shlex

def clip_video(input_video, output_video, start_time, end_time):
    # 使用ffmpeg剪辑视频
    cmd = f"ffmpeg -i {input_video} -ss {start_time} -to {end_time} -c copy {output_video}"
    subprocess.run(shlex.split(cmd))
    return output_video

if __name__ == "__main__":
    input_video = "中国工厂.mp4"
    output_video = "中国工厂_short.mp4"
    start_time = "00:00:00"
    end_time = "00:01:28"
    clip_video(input_video, output_video, start_time, end_time)
