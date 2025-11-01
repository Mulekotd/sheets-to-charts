import os
from flask import Blueprint, render_template, request, redirect, flash, send_from_directory, current_app
from app.utils.file_processor import process_uploaded_file

main_bp = Blueprint('main', __name__)

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(current_app.root_path, 'static'),
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

@main_bp.route('/')
def home():
    return render_template('index.html.jinja')

@main_bp.route('/process_file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo enviado', 'error')
        return redirect('/')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect('/')

    result = process_uploaded_file(file)
    
    if result['success']:
        return render_template('select_columns.html.jinja', columns=result['columns'])
    else:
        flash(result['message'], 'error')
        return redirect('/')
