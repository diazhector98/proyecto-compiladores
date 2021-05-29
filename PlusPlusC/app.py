import sys
sys.path.insert(0, '.')

from flask import Flask, request, json, jsonify
from compiler.lexer.lexer import PlusPlusCLexer
from compiler.parser.parser import PlusPlusCParser
from virtual_machine.file_reader import FileReader
from virtual_machine.virtual_machine import VirtualMachine
import run 

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
        # Fetch la info que viene con la key "code"
        req_data = request.get_json()
        file_text = req_data["code"]
        file_code_text = file_text

        # Parsea el codigo 
        try: 
            parser.parse(lexer.tokenize(file_code_text))
        except:
            # Si no se pudo parsear... por lo pronto solo regresa este string "Error de compilacion"
            # con la key "compiler"
            
            # Pienso que aqui regresar una variable con el contenido del error de exception
            return {"compiler": "Error de compilacion"}

        compiler_output = parser.output

        # Regresa el resultado con la key "compiler"
        return {"compiler": str(compiler_output)}
    except:
        return 'Error: La key code para compiar codigo no funciono', 400


@app.route('/runFile', methods=['POST'])
def run_File():
    try:
        # Fetch la info que viene con la key "compilerResult"
        req_data = request.get_json()
        file_result = req_data["compilerResult"]
        
        # Ejectuta el codigo y guardalo en variable result
        run.run_virtual_machine()
        result = run.virtual_machine_output
       
        # Regresa el resultado con la key "result"
        return {"result": str(result)}
    except:
        return 'Error: La key code para ejectuar codigo no funciono', 400