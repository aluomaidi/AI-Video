import requests
import datetime
import hashlib
import base64
import hmac
import json
from utils import parse_srt_file, save_srt_file
from execute_time import execute_time

class NiuTransTranslator:
    def __init__(self, app_id="e8437c4a", api_key="35586b25a94f4b4fe61889fc307eaabf", api_secret="OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl", host="ntrans.xfyun.cn"):
        self.APPID = app_id
        self.APIKey = api_key
        self.Secret = api_secret
        self.Host = host
        self.RequestUri = "/v2/ots"
        self.url = f"https://{self.Host}{self.RequestUri}"
        self.Algorithm = "hmac-sha256"

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generate_signature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        sign = self.generate_signature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self, text, from_lang='auto', to_lang='auto'):
        content = str(base64.b64encode(text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": {
                "from": from_lang,
                "to": to_lang,
            },
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        return body

    def translate(self, text, from_lang='auto', to_lang='auto'):
        self.Date = self.httpdate(datetime.datetime.utcnow())
        self.HttpMethod = "POST"
        self.HttpProto = "HTTP/1.1"

        body = self.get_body(text, from_lang, to_lang)
        headers = self.init_header(body)

        try:
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            if response.status_code == 200:
                respData = json.loads(response.text)
                return respData
            else:
                print(f"HTTP请求失败，状态码：{response.status_code}，错误信息：{response.text}")
                return None
        except Exception as e:
            print(f"请求异常：{e}")
            return None

@execute_time
def text_translate(text, from_lang='auto', to_lang='auto'):
    translator = NiuTransTranslator(app_id, api_key, api_secret)
    trans_text = translator.translate(text, from_lang, to_lang)
    return trans_text

@execute_time
def subtitle_translate(app_id, api_key, api_secret, origin_srt_file, trans_srt_file, from_lang='auto', to_lang='auto'):
    srt_data = parse_srt_file(origin_srt_file)
    translator = NiuTransTranslator(app_id, api_key, api_secret)
    trans_srt_data = []
    for index, (timestamp, text) in enumerate(srt_data):
        trans_text = translator.translate(text, from_lang, to_lang)
        dst_text = trans_text['data']['result']['trans_result']['dst']
        trans_srt_data.append((timestamp, dst_text))
    save_srt_file(trans_srt_data, trans_srt_file)            
        
if __name__ == '__main__':
    app_id = "e8437c4a"
    api_key = "35586b25a94f4b4fe61889fc307eaabf"
    api_secret = "OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl"

    origin_srt_file = "output/重庆森林片段.srt"
    trans_srt_file = "output/重庆森林片段_en.srt"
    subtitle_translate(app_id,api_key, api_secret, origin_srt_file, trans_srt_file, from_lang='zh', to_lang='en')