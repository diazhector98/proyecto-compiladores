import sys
import os
directory = os.getcwd()
compiler_folder_name = 'PlusPlusC'
compiler_directory = os.path.join(directory, compiler_folder_name)
sys.path.append(compiler_directory)

from app import app 
  
if __name__ == "__main__": 
    app.run() 