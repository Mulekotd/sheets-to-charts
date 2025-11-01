from flask import Blueprint, render_template, request, session, flash, redirect
from app.utils.chart_creator import create_chart
import pandas as pd

charts_bp = Blueprint('charts', __name__)

@charts_bp.route('/generate_chart', methods=['POST'])
def generate_chart_route():
    x_column = request.form.get('x_column')
    y_column = request.form.get('y_column')

    if not x_column or not y_column:
        flash('Selecione as colunas X e Y', 'error')
        return redirect('/')

    if 'file_data' not in session:
        flash('Dados do arquivo não encontrados.', 'error')
        return redirect('/')

    try:
        data_frame = pd.read_json(session['file_data'])
        chart = create_chart(x_column, y_column, data_frame)
        return render_template('dashboards.html.jinja', chart=chart)
    except Exception as e:
        flash(f'Erro ao gerar gráfico: {str(e)}', 'error')
        return redirect('/')
