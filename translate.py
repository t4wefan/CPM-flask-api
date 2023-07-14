
print('starting')
from transformers import AutoModelForCausalLM, AutoTokenizer
print('loading and checking model, it may take while')
tokenizer = AutoTokenizer.from_pretrained("openbmb/cpm-bee-10b", trust_remote_code=True, )
model = AutoModelForCausalLM.from_pretrained("openbmb/cpm-bee-10b", trust_remote_code=True, ).cuda()  
print("model loaded, starting server")

def translate_c2e(text):
    pending_txt = str(text)
    pending = None
    result = pending
    pending = model.generate({"input": pending_txt, 
                              "prompt": "中翻英", 
                              "<ans>": ""}, tokenizer)
    arr = pending[0]
    ans = str(arr['<ans>'])
    pending = arr 
    pending['result'] = ans
    result = pending
    print(result)
    return result

def translate_e2c(text):
    pending_txt = str(text)
    pending = None
    result = pending
    pending = model.generate({"input": pending_txt, 
                              "prompt": "英翻中", 
                              "<ans>": ""}, tokenizer)
    arr = pending[0]
    ans = str(arr['<ans>'])
    pending = arr
    pending['result'] = ans
    result = pending
    print(result)
    return result

def detect_lang(text):
    pending_txt = str(text)
    pending = None
    result = pending
    pending = model.generate({"input": pending_txt, 
                              "options": {"<option_0>": "英语", 
                                          "<option_1>": "中文", 
                                          "<option_2>": "其他语言"},
                              "question": "这段话的语言是：",
                              "<ans>": ""}, tokenizer)
    arr = pending[0]
    ans = str(arr['<ans>'])
    pending = arr
    pending['result'] = ans
    result = pending
    print(result)
    return result

def translate_to(lang, text):
    if lang in ['en', 'English','english',"英语",]:
        pending = translate_c2e(text)
        return pending
    if lang in ['ch', 'cn','Chinese','chinese',"中文",]:
        pending = translate_e2c(text)
        return pending
    else: 
        return {'status': 'error',
                'info': 'unsupported language'}

from flask import Flask, request

app = Flask(__name__)

@app.route('/translate', methods=['GET'])
def translate():
    text = request.args.get('text')
    lang = request.args.get('from')
    result0 = translate_to(lang, text)
    result = result0['result']
    return result

@app.route('/translate-full', methods=['GET'])
def translate():
    text = request.args.get('text')
    lang = request.args.get('from')
    result = translate_to(lang, text)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)