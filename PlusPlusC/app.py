import sys
sys.path.insert(0, '.')

from flask import Flask, request, json, jsonify
from compiler.lexer.lexer import PlusPlusCLexer
from compiler.parser.parser import PlusPlusCParser
from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine

app = Flask(__name__)

file_text = ""

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

        file_code_text = file_text
        parser.parse(lexer.tokenize(file_code_text))
        compiler_output = parser.output

        print("compiler_output", compiler_output)

        return {"compiler": str(compiler_output)}
    except:
        return 'Error: La key code para compiar codigo no funciono', 400


@app.route('/runFile', methods=['POST'])
def run_File():
    
    try: 
        req_data = request.get_json()
        file_result = req_data["compilerResult"]
        
        print("file_result", file_result)

        file_result_text = file_result
        virtual_machine = VirtualMachine(file_result_text,read_file=False, terminal=False)
        print("file_result2", file_result)
        
        #causa error aqui
        virtual_machine.run()
        print("file_result3", file_result)

        file_result_output = virtual_machine.output

        print("file_result_output", file_result_output)

        return {"result": str(file_result_output)}
    except:
        return 'Error: La key code para ejectuar codigo no funciono', 400