import whisper
from whisper.utils import get_writer
from execute_time import execute_time
from utils import extract_filename

@execute_time
def speech_to_text(audio, language, model='small', word_timestamps=True):
    model = whisper.load_model(model)
    if language == 'zh':
        result = model.transcribe(audio, language=language, word_timestamps=word_timestamps,initial_prompt="请转录为简体中文。")
    else :
        result = model.transcribe(audio, language=language, word_timestamps=word_timestamps)
    return result["text"]

@execute_time
def speech_to_srt(audio, language, srt_path, model='small', word_timestamps=True):
    model = whisper.load_model(model)
    if language == 'zh':
        result = model.transcribe(audio, language=language, word_timestamps=word_timestamps,initial_prompt="请转录为简体中文。")
    else :
        result = model.transcribe(audio, language=language, word_timestamps=word_timestamps)
    srt_writer = get_writer("srt", srt_path)
    srt_writer(result, audio, {"max_line_count":1,"max_line_width":20})
    _, filename = extract_filename(audio)
    return result["text"], srt_path + "/" + filename + ".srt"

if __name__ == '__main__':
    audio = '重庆森林片段.mp4'
    language = 'zh'
    srt_path = "output"
    word_timestamps = True
    model = 'medium'
    speech_to_srt(audio, language, srt_path ,word_timestamps, model) 