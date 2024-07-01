import whisper
from whisper.utils import get_writer
import time

# Record the start time
start_time = time.time()
model = whisper.load_model("medium")
# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

voice = "重庆森林片段.mp4"
# voice = "20240624104058895.mp4"

result = model.transcribe(voice,language="zh",word_timestamps=True,initial_prompt="请转录为简体中文。")
print(result["text"])

srt_writer = get_writer("srt", "./output/")
srt_writer(result, voice, {"max_line_count":1,"max_line_width":20})

# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
# Print the elapsed time
print(f"Elapsed time: {elapsed_time} seconds")

# # 加载模型（可以选择不同的模型，如 tiny, base, small, medium, large）
# model = WhisperModel("large")
# # 进行语音识别
# segments, info = model.transcribe(voice,language="zh",word_timestamps=True,initial_prompt="请转录为简体中文。")

# # 输出识别结果
# for segment in segments:
#     print(f"开始时间: {segment.start}, 结束时间: {segment.end}, 文本: {segment.text}")