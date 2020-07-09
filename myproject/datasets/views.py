from flask import Blueprint, render_template, request, redirect, url_for
from myproject import db, DATASETS_DIRECTORY
from myproject.models import Dataset
from werkzeug.utils import secure_filename
import os
import pandas as pd
#from myproject.datasets.forms import AddForm

datasets_blueprint = Blueprint('dataset',
                              __name__,
                              template_folder='templates/datasets')


def get_file_info(filename, columns_separator, coltypes, colnames):
    '''
    Funkcja zwraca obiekt z danymi dotyczącymi pliku, które będzie można dodać do bazy danych.
    '''



    dir_name = filename.split('.')[0]
    columns_filename = f'{dir_name}_column_description.csv'



    
    lines=1
    columns=1

    return Dataset(
        filename=filename,
        directory=os.path.join(DATASETS_DIRECTORY, dir_name),
        number_of_lines=lines,
        number_of_columns=columns,
        columns_separator=columns_separator,
        columns_name=str(colnames),
        columns_type=str(coltypes),
        columns_description_filename=columns_filename)


@datasets_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add_dataset.html')


@datasets_blueprint.route('/upload_result', methods=['GET','POST'])
def upload_result():
    
    columns_separator = request.form.get('col_sep', ';') # domyślna wartość to średnik
    checkbox = request.form.get('checkbox')
    colnames = request.form.get('colnames')
    if colnames:
        colnames = colnames.split(';')
    coltypes = request.form.get('coltypes')
    if coltypes:
        coltypes = coltypes.split(';')

    f = request.files["plik"]
    filename = secure_filename(f.filename)
    file_dirname = filename.split('.')[0]
    saved_dir = r'myproject/datasets/saved'
     
    if file_dirname in os.listdir(saved_dir):
        return render_template('upload_result.html', info=f'plik {filename} już istnieje')
    else:
          # jeżeli nie istnieje to tworzymy folder dla pliku
        try:
            os.mkdir(f'{saved_dir}/{file_dirname}')
        except Exception as e:
             # nie możemy stworzyć folderu, dlatego należy uznać to za błąd
            return render_template('upload_result.html',info='Nie możemy stworzyć folderu')
        # zapisujemy plik, używamy funkcji join do łączenia ścieżek
        name_with_dir = f'{saved_dir}/{file_dirname}/{filename}'
        f.save(name_with_dir)

        dataset_object = get_file_info(filename, columns_separator, coltypes, colnames)

        # TODO zapisujemy dataset_object w bazie danych
        if db.session.query(Dataset).filter_by(filename=dataset_object.filename).count() < 1:
            db.session.add(dataset_object)
            db.session.commit()
        # oraz generujemy szablon added_dataset.html z odpowiednią informacją
    return render_template('upload_result.html', dataset=dataset_object)