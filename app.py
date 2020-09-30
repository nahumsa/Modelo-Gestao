from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from dashUtils import generate_table, week_visualization

server = Flask(__name__)
# Setting the database
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servico.db'
db = SQLAlchemy(server)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_equipamento = db.Column(db.Integer, default=0)
    tipo_servico = db.Column(db.String(200), nullable=False)
    desc_servico = db.Column(db.String(200), nullable=False)    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Servico {self.id}>'

@server.route("/", methods=['POST', 'GET'])
def index():
    """Gera a página principal e posta o formulário na 
    database.
    
    """
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

@server.route("/all_tasks")    
def all_tasks():
    """Mostra todas os pedidos.
    
    """
    serv = Servico.query.order_by(Servico.date_created).all()
    return render_template('alltasks.html', servicos=serv)
    

@server.route("/delete/<int:id>")    
def delete(id):
    """Deleta um pedido na database.

    Args:
        id (int): id do pedido
    
    """
    task_to_delete = Servico.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/all_tasks")
    except:
        return "There was a problem deleting that task"


#Import css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

def database_to_dataframe():
    """Transform the database into a dataframe.
    
    """
    servicos = Servico.query.order_by(Servico.date_created).all()
    
    row_list = []
    for servico in servicos: 
        row_list.append({"IDServico": servico.id,  
                    "IDEquipamento": servico.id_equipamento, 
                    "Tipo": servico.tipo_servico, 
                    "Descricao": servico.desc_servico, 
                    "dataCriada": servico.date_created.date(), 
                    })
    df = pd.DataFrame(row_list)
    return df


df = database_to_dataframe()

series = week_visualization(df)


fig = px.histogram(df, x="dataCriada", 
                   title='Tipos por data criada',
                   labels={'dataCriada':'Data Criada'}, 
                   color="Tipo", barmode="group")

fig.update_layout(
    title_text='Tipos por data criada',     
    yaxis_title_text='Número de pedidos', 
    bargap=0.2, 
    bargroupgap=0.1 
)

fig2 = px.bar(series, x='Semana/Ano', y=0 , color='Tipo') 
fig2.update_layout(
    title_text='Visualização Semanal',     
    yaxis_title_text='Número de pedidos Semanais', 
)

app.layout = html.Div(children=[        
    dcc.Link('Homepage', href='/'),
    html.H1(children='Dashboard'),
    # generate_table(df),

    dcc.Graph(
        id='hist1',
        figure=fig
    ),
    
    dcc.Graph(
        id='bar',
        figure=fig2
    ),
        ])


if __name__ == "__main__":
    create_db = False
    add_mock = False
    if create_db: 
        db.create_all() 
    
    if add_mock:
        mock_df = pd.read_csv("MOCK_DATA.csv")           
        for i in range(mock_df.shape[0]):
            print(i)
            pedido = mock_df.iloc[i, :]          
            novo_pedido = Servico(id_equipamento=int(pedido['id_equipamento']),
                           tipo_servico=pedido['tipo_servico'],
                           desc_servico=pedido['desc_servico'],
                           date_created=datetime.strptime(pedido['date_created'], '%m/%d/%Y'),
                          )            
            db.session.add(novo_pedido)
            db.session.commit()
        exit(1)
    server.run(debug=True)  
    # app.run_server(debug=True)    
