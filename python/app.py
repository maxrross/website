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
    selected_block = request.form['block']
    structure = request.form['structure']
    size = request.form['size']
    add_H = request.form.get('pores_allowed', 'no') == 'yes'  # Convert checkbox to bool

    try:
        if selected_block == "block1":
            result = subprocess.check_output(['python', 'block1.py', size, structure, str(add_H)], universal_newlines=True)
            
        elif selected_block == "block2":
            # extract other needed parameters for block2
            coordination_number = request.form['coordination_number']
            metal_type = request.form['metal_type']
            dopant_type = request.form['dopant_type']
            dopant_number = request.form['dopant_number']
            result = subprocess.check_output(['python', 'block2.py', size, structure, coordination_number, metal_type, dopant_type, dopant_number, str(add_H)], universal_newlines=True)
            
        elif selected_block == "block3":
            # extract other needed parameters for block3
            coordination_number = request.form['coordination_number']
            metal_type = request.form['metal_type']
            dopant_type = request.form['dopant_type']
            dopant_number = request.form['dopant_number']
            vacancy_type = request.form['vacancy_type']
            result = subprocess.check_output(['python', 'block3.py', size, structure, coordination_number, metal_type, dopant_type, dopant_number, vacancy_type, str(add_H)], universal_newlines=True)

        files = os.listdir("output")  # get a list of files in the output directory
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
