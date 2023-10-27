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

def get_all_files_in_directory(directory):
    """Recursively get all files in a directory."""
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.relpath(os.path.join(dirpath, f), directory)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    structure = request.form.get('structure')
    size = request.form.get('size')
    add_H = str(request.form.get('pores_allowed', 'no') == 'yes')  # Convert checkbox to bool, then to string
    
    try:
        # Check for Block 1 form data
        if structure and size:
            result = subprocess.check_output(['python', 'scripts/block1.py', size, structure, add_H], universal_newlines=True)

        # Check for Block 2 form data
        elif 'metal_type' in request.form:
            coordination_number = request.form['coordination_number']
            metal_type = request.form['metal_type']
            dopant_type = request.form['dopant_type']
            dopant_number = str(len(dopant_type.split(',')))
            result = subprocess.check_output(['python', 'scripts/block2.py', size, structure, coordination_number, metal_type, dopant_type, dopant_number, add_H], universal_newlines=True)

        # Check for Block 3 form data
        elif 'defect_type' in request.form:
            defect_type = request.form['defect_type']
            result = subprocess.check_output(['python', 'scripts/block3.py', size, structure, coordination_number, metal_type, dopant_type, dopant_number, defect_type, add_H], universal_newlines=True)

        else:
            return render_template('error.html', error_message="Invalid form submission.")

        files = list(get_all_files_in_directory("output"))  # get a list of all files, including nested ones
        return render_template('result.html', result=result, files=files)
        
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

@app.route('/output/<path:filename>')
def serve_file(filename):
    """Serve files from the output directory"""
    return send_from_directory("output", filename, as_attachment=True)
    
if __name__ == '__main__':
    app.run(debug=True)
