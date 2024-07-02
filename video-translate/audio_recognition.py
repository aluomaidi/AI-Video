import whisper
from whisper.utils import get_writer
import time
from text_translation import  NiuTransTranslator
# Record the start time
start_time = time.time()
model = whisper.load_model("large")
# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
# Print the elapsed time
print(f"模型加载时间: {elapsed_time} seconds")

voice = "重庆森林片段.mp4"
# voice = "20240624104058895.mp4"

# Record the start time
start_time = time.time()

result = model.transcribe(voice,language="zh",word_timestamps=True,initial_prompt="请转录为简体中文。")
print(result["text"])
segments =result["segments"]
translator = NiuTransTranslator()
if segments:
    for segment in segments:
        recognized_text = segment['text']
        trans_text = translator.translate(recognized_text, from_lang='zh', to_lang='en')
        dst_text = trans_text['data']['result']['trans_result']['dst']
        print("翻译前：" + recognized_text + "翻译后：" + dst_text)

srt_writer = get_writer("srt", "./output/")
srt_writer(result, voice, {"max_line_count":1,"max_line_width":20})

# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
# Print the elapsed time
print(f"语音识别时间: {elapsed_time} seconds")