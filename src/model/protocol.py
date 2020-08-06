import json
from .message import ZapMessage

def ZapMessageDecode(text):
    try:
        data = json.loads(text.decode('utf-8'))
        return ZapMessage(data['sender'], data['receiver'], data['content'])
    except Exception as exc:
        print(exc)

def ZapMessageEncode(zap_message):
    return json.dumps(zap_message.__dict__).encode()
