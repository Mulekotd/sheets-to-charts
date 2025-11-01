from pychartjs import BaseChart, ChartType, Color
import numpy as np

def create_chart(x_column, y_column, data_frame, chart_type='bar'):
    x_data = data_frame[x_column].tolist()
    
    # Handle different data types for Y column
    if data_frame[y_column].dtype == 'O':
        # Try to convert string to float (handle currency, percentages, etc.)
        y_data = data_frame[y_column].str.replace(',', '').str.replace('R$', '').str.replace('%', '').astype(float).tolist()
    else:
        y_data = data_frame[y_column].tolist()

    class EnhancedChart(BaseChart):
        type = ChartType.Bar
        
        data = {
            'labels': x_data,
            'datasets': [{
                'label': y_column,
                'data': y_data,
                'backgroundColor': Color.Blue,
                'borderColor': Color.Blue,
                'borderWidth': 2,
                'fill': False,
                'tension': 0.4,  # Smooth lines
                'pointRadius': 5,
                'pointHoverRadius': 8,
                'pointBackgroundColor': Color.Blue,
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2,
            }],
        }
        
        options = {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {
                    'display': True,
                    'position': 'top',
                },
                'tooltip': {
                    'mode': 'index',
                    'intersect': False,
                }
            },
            'scales': {
                'xAxes': [{
                    'display': True,
                    'gridLines': {
                        'display': True,
                        'color': 'rgba(0, 0, 0, 0.05)'
                    },
                    'ticks': {
                        'beginAtZero': True
                    }
                }],
                'yAxes': [{
                    'display': True,
                    'gridLines': {
                        'display': True,
                        'color': 'rgba(0, 0, 0, 0.05)'
                    },
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            }
        }

    return EnhancedChart()


def create_statistical_chart(x_column, y_column, data_frame, chart_type='scatter'):
    x_data = data_frame[x_column].tolist()
    
    if data_frame[y_column].dtype == 'O':
        y_data = data_frame[y_column].str.replace(',', '').astype(float).tolist()
    else:
        y_data = data_frame[y_column].tolist()
    
    # Calculate regression line
    if len(x_data) > 1 and all(isinstance(x, (int, float)) for x in x_data):
        x_numeric = np.array(range(len(x_data)))
        y_numeric = np.array(y_data)
        
        # Linear regression
        coefficients = np.polyfit(x_numeric, y_numeric, 1)
        regression_line = np.polyval(coefficients, x_numeric).tolist()
    else:
        regression_line = None
    
    # Prepare scatter data
    scatter_data = [{'x': i, 'y': y} for i, y in enumerate(y_data)]
    
    datasets = [{
        'label': y_column,
        'data': scatter_data,
        'backgroundColor': 'rgba(172, 24, 24, 0.6)',
        'borderColor': 'rgba(172, 24, 24, 1)',
        'pointRadius': 6,
        'pointHoverRadius': 8,
    }]
    
    # Add regression line if calculated
    if regression_line:
        datasets.append({
            'label': 'Linha de Tendência',
            'data': regression_line,
            'type': 'line',
            'borderColor': 'rgba(231, 76, 60, 0.8)',
            'borderWidth': 2,
            'borderDash': [5, 5],
            'fill': False,
            'pointRadius': 0,
        })
    
    class StatisticalChart(BaseChart):
        type = ChartType.Scatter
        
        data = {
            'labels': x_data,
            'datasets': datasets
        }
        
        options = {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {
                    'display': True,
                    'position': 'top',
                }
            },
            'scales': {
                'xAxes': [{
                    'type': 'linear',
                    'position': 'bottom',
                    'scaleLabel': {
                        'display': True,
                        'labelString': x_column
                    }
                }],
                'yAxes': [{
                    'scaleLabel': {
                        'display': True,
                        'labelString': y_column
                    }
                }]
            }
        }
    
    return StatisticalChart()


def create_multi_series_chart(data_frame, x_column, y_columns, chart_type='line'):
    x_data = data_frame[x_column].tolist()
    
    colors = [
        'rgba(172, 24, 24, 0.8)',
        'rgba(52, 152, 219, 0.8)',
        'rgba(46, 204, 113, 0.8)',
        'rgba(155, 89, 182, 0.8)',
        'rgba(241, 196, 15, 0.8)',
    ]
    
    datasets = []
    for idx, y_col in enumerate(y_columns):
        if data_frame[y_col].dtype == 'O':
            y_data = data_frame[y_col].str.replace(',', '').astype(float).tolist()
        else:
            y_data = data_frame[y_col].tolist()
        
        color = colors[idx % len(colors)]
        
        datasets.append({
            'label': y_col,
            'data': y_data,
            'backgroundColor': color,
            'borderColor': color.replace('0.8', '1'),
            'borderWidth': 2,
            'fill': False,
            'tension': 0.4,
        })
    
    class MultiSeriesChart(BaseChart):
        type = ChartType.Line
        
        data = {
            'labels': x_data,
            'datasets': datasets
        }
        
        options = {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {
                    'display': True,
                    'position': 'top',
                }
            },
            'scales': {
                'xAxes': [{
                    'display': True,
                }],
                'yAxes': [{
                    'display': True,
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            }
        }
    
    return MultiSeriesChart()
