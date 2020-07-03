from myproject import db

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nazwa pliku
    # unique=True powoduje, że w całej tabeli może istnieć tylko jeden rekord z daną nazwą pliku
    filename = db.Column(db.String(80), unique=True, nullable=False)
    # folder w którym jest przechowywany plik
    directory = db.Column(db.String(80), unique=True, nullable=False)
    number_of_lines = db.Column(db.Integer, nullable=False)
    # jakim znakiem są rozdzielane kolumny w pliku?
    columns_separator = db.Column(db.String(1), nullable=False)
    number_of_columns = db.Column(db.Integer, nullable=False)
    # nazwa pliku z opisem kolumn - będzie dodany później, po zajęciach z pandas
    columns_description_filename = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Zbiór danych {self.filename}, ({self.number_of_lines} x {self.number_of_columns})>'
