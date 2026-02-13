from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Article('{self.content}','{self.date_posted}')" 

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Article.query.get_or_404(id)
    try:    
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"There was an issue deleting your task: {str(e)}"
        

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=Article.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form.get('task')
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"There was an issue updating your task: {str(e)}"
    else:
        return render_template('update.html',task=task)


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        task_content = request.form.get('task')
        if not task_content:
            return "Task content cannot be empty"
        new_task=Article(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"There was an issue adding your task: {str(e)}"    
    else:
        tasks=Article.query.order_by(Article.date_posted.desc()).all()
        return render_template('index.html',tasks=tasks)

with app.app_context():
    db.create_all()

if __name__=='__main__':
    app.run(debug=True)