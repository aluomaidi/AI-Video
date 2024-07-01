from googletrans import Translator

text = "我是一个中国人，我爱我的祖国，我爱我的家人，我努力工作，照顾家人，报效祖国！"
# 使用 Google Translate 进行翻译
translator = Translator()
translation = translator.translate(text, src='zh-CN', dest='en')

# 打印翻译结果
print("翻译文本:", translation.text)