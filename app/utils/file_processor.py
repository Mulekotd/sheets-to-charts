import pandas as pd
from flask import session
from datetime import datetime
import os

def process_uploaded_file(file):
    filename = file.filename
    file_extension = filename.split('.')[-1].lower()
    
    if file_extension == 'csv':
        engine = 'python'
    elif file_extension in ['xlsx', 'xls']:
        engine = None
    else:
        return {
            'success': False,
            'message': 'Formato de arquivo não suportado. Use .csv, .xlsx ou .xls'
        }

    try:
        # Read file based on type
        if engine == 'python':
            df = pd.read_csv(file, encoding='utf-8')
        else:
            df = pd.read_excel(file)

        # Get file metadata
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        # Get column information
        columns = df.columns.tolist()
        column_types = {col: str(df[col].dtype) for col in columns}
        
        # Calculate basic statistics
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        stats = {}
        
        for col in numeric_columns:
            stats[col] = {
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median())
            }
        
        # Store data in session
        session['file_data'] = df.to_json()
        session['file_metadata'] = {
            'filename': filename,
            'size': file_size,
            'type': file_extension.upper(),
            'rows': len(df),
            'columns': len(columns),
            'column_types': column_types,
            'upload_time': datetime.now().isoformat()
        }

        return {
            'success': True,
            'columns': columns,
            'metadata': session['file_metadata'],
            'stats': stats,
            'message': f'Arquivo processado com sucesso: {len(df)} linhas, {len(columns)} colunas'
        }

    except UnicodeDecodeError:
        # Try alternative encodings for CSV
        if engine == 'python':
            try:
                file.seek(0)
                df = pd.read_csv(file, encoding='latin-1')
                columns = df.columns.tolist()
                session['file_data'] = df.to_json()
                
                return {
                    'success': True,
                    'columns': columns,
                    'message': 'Arquivo processado com sucesso (codificação alternativa)'
                }
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Erro de codificação: {str(e)}'
                }
        else:
            return {
                'success': False,
                'message': 'Erro ao ler arquivo Excel'
            }
    
    except pd.errors.EmptyDataError:
        return {
            'success': False,
            'message': 'O arquivo está vazio'
        }
    
    except pd.errors.ParserError as e:
        return {
            'success': False,
            'message': f'Erro ao analisar arquivo CSV: {str(e)}'
        }
    
    except Exception as e:
        return {
            'success': False,
            'message': f'Erro ao processar arquivo: {str(e)}'
        }


def format_file_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = size_bytes
    
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.2f} {size_names[i]}"


def validate_columns(df, x_column, y_column):
    errors = []
    
    if x_column not in df.columns:
        errors.append(f'Coluna X "{x_column}" não encontrada')
    
    if y_column not in df.columns:
        errors.append(f'Coluna Y "{y_column}" não encontrada')
    
    if not errors:
        # Check if Y column contains numeric data
        if df[y_column].dtype == 'object':
            # Try to convert to numeric
            try:
                pd.to_numeric(df[y_column].str.replace(',', ''))
            except:
                errors.append(f'Coluna Y "{y_column}" não contém dados numéricos válidos')
    
    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def get_recommended_chart_type(df, x_column, y_column):
    x_is_numeric = pd.api.types.is_numeric_dtype(df[x_column])
    y_is_numeric = pd.api.types.is_numeric_dtype(df[y_column])
    
    x_unique = df[x_column].nunique()
    total_rows = len(df)
    
    # Recommendation logic
    if x_unique <= 10:
        if y_is_numeric:
            return 'bar'  # Few categories, numeric values - bar chart
    elif x_unique > 20:
        if x_is_numeric and y_is_numeric:
            return 'scatter'  # Many numeric values - scatter plot
        else:
            return 'line'  # Time series or trend data
    else:
        return 'line'  # Medium number of categories - line chart
    
    return 'bar'  # Default
