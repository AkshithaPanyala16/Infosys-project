import os
import re
import cv2
import shutil
import pandas as pd
from flask import Flask, request, jsonify, send_file, render_template
from fuzzywuzzy import fuzz, process

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULTS_FOLDER'] = 'results/'
DATABASE_PATH = 'fraud aadhar detection'

def removeDb():
    if os.path.exists(DATABASE_PATH):
        try:
            os.remove(DATABASE_PATH)
            return jsonify({"message": "Database file deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to delete database file: {str(e)}"}), 500
    else:
        return jsonify({"message": "Database file does not exist"}), 404

def delete_uploads(upload_folder):
    try:
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return jsonify({"message": "Uploads folder contents deleted successfully"}), 200
        else:
            return jsonify({"message": "Uploads folder does not exist"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete uploads folder contents: {str(e)}"}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    removeDb()
    delete_uploads(app.config['UPLOAD_FOLDER'])
    
    if 'zipfile' not in request.files or 'excelfile' not in request.files:
        return jsonify({"error": "Both ZIP and Excel files are required"}), 400

    zip_file = request.files['zipfile']
    excel_file = request.files['excelfile']
    
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_file.filename)
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_file.filename)
    
    zip_file.save(zip_path)
    excel_file.save(excel_path)
    
    return jsonify({"message": "Files uploaded successfully"}), 200

@app.route('/download', methods=['GET'])
def download_results():
    file_path = os.path.join(app.config['RESULTS_FOLDER'], 'results.xlsx')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "Results file not found"}), 404

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
