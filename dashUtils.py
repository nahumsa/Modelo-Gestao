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

def week_visualisation(df):
    df['Semana/Ano'] = df['dataCriada'].apply(lambda x: "%d/%d" % (x.isocalendar()[1], x.year))
    return df.groupby(['Semana/Ano' , 'Tipo']).size().reset_index()