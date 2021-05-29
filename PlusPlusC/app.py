
import sys
sys.path.insert(0, '.')

from flask import Flask, request, json, jsonify
from compiler.lexer.lexer import PlusPlusCLexer
from compiler.parser.parser import PlusPlusCParser

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return {"value": "Hello, World!"}

@app.route('/compileFile', methods=['POST'])
def compile_File():
    lexer = PlusPlusCLexer()
    parser = PlusPlusCParser()
    try: 
        req_data = request.get_json()
        file_text = req_data["code"]
        
        print("input_text", file_text)

        text = file_text
        parser.parse(lexer.tokenize(text))
        compiler_output = parser.output

        print("output_text", compiler_output)

        return {"value": str(compiler_output)}
    except:
        return 'Error: La key code no funciono', 400