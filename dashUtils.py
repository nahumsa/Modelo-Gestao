import dash_html_components as html
import pandas as pd

def generate_table(dataframe, max_rows=10):
    """ Generate a html table for a given dataframe
    """
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

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