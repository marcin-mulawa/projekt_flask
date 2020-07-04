from myproject import app, db
from flask import render_template


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':

    db.create_all()
    
    app.run(debug=True)