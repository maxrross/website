import os
import sys
import subprocess
from flask import Flask, render_template, request, send_from_directory



# Add the 'lib' directory to the Python module search path
lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib')
sys.path.insert(0, lib_dir)

# Now you can import the required packages locally
import NPC
import numpy as np
from tqdm import tqdm
from itertools import combinations

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    structure = request.form['structure']
    size = request.form['size']
    vacancies = request.form['vacancies']
    pores_allowed = request.form['pores_allowed']
    output_structures = request.form['output_structures']
    
    try:
        result = subprocess.check_output(['python', 'multi_vacancy_generator.py', structure, size, vacancies, pores_allowed, output_structures], universal_newlines=True)
        files = os.listdir("output") # get a list of files in the output directory
        return render_template('result.html', result=result, files=files)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

@app.route('/output/<path:filename>')
def serve_file(filename):
    """Serve files from the output directory"""
    return send_from_directory("output", filename, as_attachment=True)
    
if __name__ == '__main__':
    app.run()
