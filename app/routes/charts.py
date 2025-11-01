from flask import Blueprint, render_template, request, session
from app.utils.chart_creator import create_chart
import pandas as pd

main_bp = Blueprint('main', __name__)
charts_bp = Blueprint('charts', __name__)

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

@charts_bp.route('/generate_chart', methods=['POST'])
def generate_chart_route():
    x_column = request.form['x_column']
    y_column = request.form['y_column']

    if 'file_data' not in session:
        return "Dados do arquivo não encontrados.", 400

    data_frame = pd.read_json(session['file_data'])
    chart = create_chart(x_column, y_column, data_frame)

    return render_template('dashboards.html.jinja', chart=chart)