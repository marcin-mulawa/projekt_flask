from flask import Blueprint,render_template,redirect,url_for
from myproject import db
from myproject.models import File
from myproject.files.forms import AddForm

files_blueprint = Blueprint('files',
                              __name__,
                              template_folder='templates/files')

@files_blueprint.route('/add', methods=['GET', 'POST'])
def add():

    form = AddForm()

    if form.validate_on_submit():
        files = form.files.data
        
        #new_file = File(name,path,...)
        #db.session.add(new_file)
        #db.session.commit()

        return redirect(url_for('files_list.html'))
    return render_template('add_file.html',form=form)
