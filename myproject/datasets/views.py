from flask import Blueprint, render_template, request, redirect, url_for
from myproject import db, DATASETS_DIRECTORY
from myproject.models import Dataset
from werkzeug.utils import secure_filename
import os
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

#from myproject.datasets.forms import AddForm

datasets_blueprint = Blueprint('dataset',
                              __name__,
                              template_folder='templates/datasets')


# Funkcja odpowiadająca za utworzenie i zapisanie histogramu
def histogram(df,column,dir_name):
    plt.figure(figsize=(8, 8))
    fig = plt.hist(df[column], bins=50)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value', fontsize=15)
    plt.ylabel('Frequency', fontsize=15)
    plt.xlim(0, max(df[column]))
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.ylabel('Frequency', fontsize=15)
    plt.title(column.upper(), fontsize=15)
    plt.savefig(f'{DATASETS_DIRECTORY}/{dir_name}/{column}_hist.png')

# Funkcje zapisu ze względu na typ danych:
# Dane typu object
def get_object(df,column):
    nulls = df[column].isnull().sum()
    types = df[column].dtypes
    uniques = df[column].nunique()
    return f'{column};{types};{uniques};'

# Dane typu liczbowego
def get_nums(df,column,dir_name):
    desc = df[column].describe().loc[['min', 'mean', 'max', '50%', 'std']]
    types = df[column].dtypes
    histogram(df,column, dir_name)
    return f'{column};{types};{desc[0]};{desc[1]};{desc[2]};{desc[3]};{desc[4]};{DATASETS_DIRECTORY}/{dir_name}/{column}_hist.png'

# Dane typu Category
def get_cat(df,column,dir_name):
    uniques = df[column].nunique()
    types = df[column].dtypes
    histogram(df,column, dir_name)
    return f'{column};{types};{uniques};{DATASETS_DIRECTORY}/{dir_name}/{column}_hist.png'

# Dane typu boolean (wymaga ręcznego rozpisania histogramu ze względu na typ [konwersja '1' i '0' na float])
def get_bool(df,column,dir_name):
    uniques = df[column].nunique()
    types = df[column].dtypes
    fig = plt.hist((df[column].astype(float)), bins=30)
    plt.title(column)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig(column + '_hist.png')
    return f'{column};{types};{DATASETS_DIRECTORY}/{dir_name}/{column}_hist.png'

# Dane typu date:
def get_date(df,column):
    types = df[column].dtypes
    mini = df[column].min()
    maxi = df[column].max()
    return f'{column};{types};{mini};{maxi}'


def get_file_info(filename, columns_separator, coltypes=None, colnames=None):
    '''
    Funkcja zwraca obiekt z danymi dotyczącymi pliku, które będzie można dodać do bazy danych.
    '''
    dir_name = filename.split('.')[0]
    
    info = ''

    columns_filename = f'{DATASETS_DIRECTORY}/{dir_name}/{dir_name}_column_description.csv'
    if colnames:
        df = pd.read_csv(f'{DATASETS_DIRECTORY}/{dir_name}/{filename}', names=colnames, sep=columns_separator)
    else:
        df = pd.read_csv(f'{DATASETS_DIRECTORY}/{dir_name}/{filename}', sep=columns_separator)
        colnames = list(df.columns)

    print(type(coltypes))
    if coltypes !="":
        for column, types in zip(df, coltypes):
            try:
                if types == 'date':
                    df[column] = pd.to_datetime(df[column])
                else:
                    df[column] = df[column].astype(types)
                    print(df[column].dtypes)
            except ValueError:
                info += f' Nie udało się przekonwertować kolumny {column} na {types}'
                df[column] = df[column].astype(str)
                
    #Zapisanie pliku do formatu .pkl
    filename = dir_name + ".pkl"
    df.to_pickle(f'{DATASETS_DIRECTORY}/{dir_name}/{filename}')


    # W tym miejscu następuje zapisanie statystyk do pliku csv
    with open(columns_filename, 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=' ',
                                escapechar=' ', quoting=csv.QUOTE_NONE)
        print(df)
        for column in df:
            print(column)
            if df[column].dtypes == 'object':
                datawriter.writerow([get_object(df,column)])

            elif df[column].dtypes == 'bool':
                datawriter.writerow([get_bool(df,column,dir_name)])

            elif df[column].dtype.name == 'category':
                datawriter.writerow([get_cat(df,column,dir_name)])

            #elif df[column].dtypes == 'float64' or df[column].dtypes == 'int64':
            elif np.issubdtype(df[column].dtype, np.number):
                datawriter.writerow([get_nums(df,column,dir_name)])

            elif df[column].dtypes == 'datetime64[ns]':
                datawriter.writerow([get_date(df,column)])

    lines = len(df)
    columns = len(df.columns)

    return info, Dataset(
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

    if request.method == 'POST':
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
        # Sprawdzamy czy folder z plikiem już istnieje
        if file_dirname in os.listdir(saved_dir):
            # jeżeli tak to wyswietlamy info że plik istnieje
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

            info, dataset_object = get_file_info(filename, columns_separator, coltypes, colnames)
            print(dataset_object)
            if os.path.exists(name_with_dir):
                try:
                    os.remove(name_with_dir)
                except: 
                    pass
            # TODO zapisujemy dataset_object w bazie danych
            if db.session.query(Dataset).filter_by(filename=dataset_object.filename).count() < 1:
                db.session.add(dataset_object)
                db.session.commit()
            # oraz generujemy szablon added_dataset.html z odpowiednią informacją
        
        return render_template('upload_result.html', dataset=dataset_object, info=info)
        

@datasets_blueprint.route('/details/<filename>', methods=['GET', 'POST'])
def details(filename):
    dir_name = filename.split('.')[0]
    df = pd.read_csv(f'{DATASETS_DIRECTORY}/{dir_name}/{dir_name}_column_description.csv', sep=';')
    return render_template("details.html", table = df)


@datasets_blueprint.route('/list', methods=['GET', 'POST'])
def list_datasets():
    # pobieramy wszystkich użytkowników z bazy do zmiennej all_users
    datasets = db.session.query(Dataset).all()
    # zwracamy szblon list_users.html podając listę ze wszystkimi użytkownikami
    return render_template('list_datasets.html', datasets=datasets)


@datasets_blueprint.route('/remove_result')
def remove_result():
    pass
