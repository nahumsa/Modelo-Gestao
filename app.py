from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Setting the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servico.db'
db = SQLAlchemy(app)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(db.Integer, default=0)
    tipo_servico = db.Column(db.String(200), nullable=False)
    desc_servico = db.Column(db.String(200), nullable=False)    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Servico {self.id}>'

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ser_id_equipamento = request.form["id_equipamento"]
        ser_tipo_servico = request.form["tipo_servico"]
        ser_desc_servico = request.form["desc_servico"]
        novo_pedido = Servico(id_equipamento=ser_id_equipamento,
                           tipo_servico=ser_tipo_servico,
                           desc_servico=ser_desc_servico,
                          )

        try:
            db.session.add(novo_pedido)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    
    else:
        serv = Servico.query.order_by(Servico.date_created).all()
        return render_template('index.html', servicos=serv)

@app.route("/all_tasks")    
def all_tasks():
    serv = Servico.query.order_by(Servico.date_created).all()
    return render_template('alltasks.html', servicos=serv)
    

@app.route("/delete/<int:id>")    
def delete(id):
    task_to_delete = Servico.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/all_tasks")
    except:
        return "There was a problem deleting that task"

# @app.route("/update/<int:id>", methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try: 
#             db.session.commit()
#             return redirect('/')
        
#         except:
#             return "there was an issue updating your task"
#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    create_db = False
    if create_db: 
        db.create_all()
    app.run(debug=True)    
