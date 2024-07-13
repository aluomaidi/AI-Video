import requests
import datetime
import hashlib
import base64
import hmac
import json
from utils import parse_srt_file, save_srt_file, extract_filename
from execute_time import execute_time
from wsgiref.handlers import format_date_time
from time import mktime
from urllib.parse import urlencode
from datetime import datetime


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

class XFTranslator:
    def __init__(self, app_id="e8437c4a", api_secret="OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl", api_key="35586b25a94f4b4fe61889fc307eaabf", res_id="its_en_cn_word"):
        self.APPId = app_id
        self.APISecret = api_secret
        self.APIKey = api_key
        self.RES_ID = res_id
        self.url = 'https://itrans.xf-yun.com/v1/its'

    def sha256base64(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def parse_url(self, request_url):
        stidx = request_url.index("://")
        host = request_url[stidx + 3:]
        schema = request_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise ValueError("invalid request url: " + request_url)
        path = host[edidx:]
        host = host[:edidx]
        return host, path, schema

    def assemble_ws_auth_url(self, request_url, method="POST"):
        host, path, schema = self.parse_url(request_url)
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"{}\", algorithm=\"hmac-sha256\", headers=\"host date request-line\", signature=\"{}\"".format(
            self.APIKey, signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }
        return request_url + "?" + urlencode(values)

    def translate(self, text, from_lang="cn", to_lang="en"):
        if from_lang == "zh":
            from_lang = "cn"
        if to_lang == "zh":
            to_lang = "cn"    
        body = {
            "header": {
                "app_id": self.APPId,
                "status": 3,
                "res_id": self.RES_ID
            },
            "parameter": {
                "its": {
                    "from": from_lang,
                    "to": to_lang,
                    "result": {}
                }
            },
            "payload": {
                "input_data": {
                    "encoding": "utf8",
                    "status": 3,
                    "text": base64.b64encode(text.encode("utf-8")).decode('utf-8')
                }
            }
        }

        request_url = self.assemble_ws_auth_url(self.url, "POST")
        headers = {'content-type': "application/json", 'host': 'itrans.xf-yun.com', 'app_id': self.APPId}
        response = requests.post(request_url, data=json.dumps(body), headers=headers)
        tempResult = json.loads(response.content.decode())
        base64.b64decode(tempResult['payload']['result']['text']).decode()
        respData = json.loads(base64.b64decode(tempResult['payload']['result']['text']).decode())
        return  respData
    
@execute_time
def text_translate(text, from_lang='auto', to_lang='auto'):
    translator = NiuTransTranslator()
    trans_text = translator.translate(text, from_lang, to_lang)
    return trans_text['data']['result']['trans_result']['dst']

@execute_time
def subtitle_translate_niu(origin_srt_file, trans_srt, from_lang='auto', to_lang='auto'):
    srt_data = parse_srt_file(origin_srt_file)
    translator = NiuTransTranslator()
    trans_srt_data = []
    for index, (timestamp, text) in enumerate(srt_data):
        trans_text = translator.translate(text, from_lang, to_lang)
        dst_text = trans_text['data']['result']['trans_result']['dst']
        trans_srt_data.append((timestamp, dst_text))
    save_srt_file(trans_srt_data, trans_srt)
    return trans_srt   

@execute_time
def subtitle_translate_xf(origin_srt_file, trans_srt, from_lang='auto', to_lang='auto'):
    srt_data = parse_srt_file(origin_srt_file)
    translator = XFTranslator()
    trans_srt_data = []
    for index, (timestamp, text) in enumerate(srt_data):
        trans_text = translator.translate(text, from_lang, to_lang)
        dst_text = trans_text['trans_result']['dst']
        trans_srt_data.append((timestamp, dst_text))
    save_srt_file(trans_srt_data, trans_srt)
    return trans_srt        
        
if __name__ == '__main__':
    # app_id = "e8437c4a"
    # api_key = "35586b25a94f4b4fe61889fc307eaabf"
    # api_secret = "OGEzZTI5ZjlkNmE3OTg2ZGNlZGY1YzJl"

    # origin_srt_file = "output/重庆森林片段.srt"
    # trans_srt_file = "output/重庆森林片段_en.srt"
    # subtitle_translate(app_id,api_key, api_secret, origin_srt_file, trans_srt_file, from_lang='zh', to_lang='en')

    translator = XFTranslator()
    translated_text = translator.translate("科大讯飞", "zh", "en")
    print('翻译结果:', translated_text)