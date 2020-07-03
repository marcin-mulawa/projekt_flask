from flask import Blueprint, render_template, request, redirect, url_for
from myproject import db, DATASETS_DIRECTORY
from myproject.models import Dataset
from werkzeug.utils import secure_filename
import os
#from myproject.datasets.forms import AddForm

datasets_blueprint = Blueprint('dataset',
                              __name__,
                              template_folder='templates/datasets')


def get_file_info(filename, columns_separator):
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
        columns_description_filename=columns_filename)


@datasets_blueprint.route('/add', methods=['GET', 'POST'])
def add():

    #form = AddForm()

    #if form.validate_on_submit():
      #  datasets = form.datasets.data
        
        #new_file = File(name,path,...)
        #db.session.add(new_file)
        #db.session.commit()

        #return redirect(url_for('show_datasets.html'))
    return render_template('add_dataset.html')


@datasets_blueprint.route('/upload_result', methods=['GET','POST'])
def upload_result():
    
    columns_separator = request.form.get('col_sep', ';') # domyślna wartość to średnik
    f = request.files["plik"]
    print(f)
    filename = secure_filename(f.filename)
    dirname = filename.split('.')[0]
     
    #if dirname in os.listdir('myproject/datasets/saved'):
    #return redirect(f"/datasets/upload_result?file={filename}&error=1")
    #else:
    dataset_object = get_file_info(filename, columns_separator)
        #  # jeżeli nie istnieje to tworzymy folder dla pliku
        # try:
        #     os.mkdir(f'myproject/datasets/saved/{filename}')
        # except Exception as e:
        #     # nie możemy stworzyć folderu, dlatego należy uznać to za błąd
        #     return redirect(f'/datasets/upload_result?file={filename}&error=2')
        # zapisujemy plik, używamy funkcji join do łączenia ścieżek
        #name_with_dir = os.path.join(dataset_object.directory, dataset_object.filename)
        #f.save(name_with_dir)
        # TODO zapisujemy dataset_object w bazie danych
        #db.session.add(dataset_object)
        #db.session.commit()
        # oraz generujemy szablon added_dataset.html z odpowiednią informacją
    return redirect(f'/datasets/upload_result?file={filename}')