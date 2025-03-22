import os
import json
from googletrans import Translator
import nbformat

def traducir_notebook(ruta_entrada, ruta_salida):
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    
    # Cargar el notebook
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    translator = Translator()
    
    # Traducir contenido
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            try:
                translated = translator.translate(cell.source, src='en', dest='es').text
                cell.source = translated
            except Exception as e:
                print(f"Error en celda {cell.id}: {str(e)}")
                continue
                
        if cell.cell_type == "code":
            new_source = []
            for line in cell.source.split('\n'):
                if line.lstrip().startswith('#'):
                    try:
                        trad = translator.translate(line, src='en', dest='es').text
                        new_source.append(trad)
                    except:
                        new_source.append(line)
                else:
                    new_source.append(line)
            cell.source = '\n'.join(new_source)
    
    # Guardar archivo traducido
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)

# Configuración específica para tus rutas
input_dir = r'C:\Users\alexis.veloz\OneDrive - Instituto Superior Tecnológico España\Escritorio\Documentos\UIDE\bettercap\CLASE2\Python-Text-Analysis-main\Python-Text-Analysis-main\lessons'
output_dir = r'C:\Users\alexis.veloz\OneDrive - Instituto Superior Tecnológico España\Escritorio\Documentos\UIDE\bettercap\CLASE2\Python-Text-Analysis-main\Python-Text-Analysis-main\lessons\Traducido'
filename = '02_bag_of_words.ipynb'

# Ejecutar traducción
traducir_notebook(
    ruta_entrada=os.path.join(input_dir, filename),
    ruta_salida=os.path.join(output_dir, filename)
)

print(f"Traducción completada: {os.path.join(output_dir, filename)}")