from myproject import app, db
from flask import render_template
import os

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':

    db.create_all()
    try:
        os.mkdir(f'myproject/datasets/saved')
    except Exception as e:
        pass
    app.run(debug=True)
