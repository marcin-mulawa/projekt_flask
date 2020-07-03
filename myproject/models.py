from myproject import db

class File(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.Text)

    file_id = db.Column(db.Integer,db.ForeignKey('files.id'))

    def __init__(self,name,):
        self.name = name
        self.file_id = fi_id

    def __repr__(self):
        return f"File Name: {self.name}"
