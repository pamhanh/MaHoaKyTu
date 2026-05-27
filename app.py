from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS # Can cai dat: pip install flask-cors

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.root_path, 'index.html')

def mod(n, m):
    return ((n % m) + m) % m

def caesar_process(text, k, action):
    shift = k if action == "encrypt" else -k
    result = ""
    for ch in text:
        if 'A' <= ch <= 'Z':
            result += chr(mod(ord(ch) - 65 + shift, 26) + 65)
        elif 'a' <= ch <= 'z':
            result += chr(mod(ord(ch) - 97 + shift, 26) + 97)
        else:
            result += ch
    return result

def vigenere_process(text, key, action):
    k_clean = "".join(filter(str.isalpha, key.lower()))
    if not k_clean: return text
    
    result = ""
    i = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(k_clean[i % len(k_clean)]) - 97
            shift = shift if action == "encrypt" else -shift
            base = 65 if ch.isupper() else 97
            result += chr(mod(ord(ch) - base + shift, 26) + base)
            i += 1
        else:
            result += ch
    return result

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    mode = data.get('mode')
    action = data.get('action')
    text = data.get('text', '')
    
    if mode == "caesar":
        k = int(data.get('k', 0))
        res = caesar_process(text, k, action)
    else:
        v_key = data.get('vKey', '')
        res = vigenere_process(text, v_key, action)
        
    return jsonify({"result": res})

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)
