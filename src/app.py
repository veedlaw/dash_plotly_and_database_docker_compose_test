import dash
from dash import dcc, html, Input, Output, State
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os

db_host = os.environ.get('DB_HOST', 'localhost')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_name = os.environ.get('DB_NAME', 'test_db')

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='dropdown'),
    html.Div(children=[
        dcc.Input(id='input-new-entry', type='text', placeholder='Enter new entry'),
        html.Button('Add Entry', id='button-add-entry', n_clicks=0),
        html.Div(id='container-button'),
        html.Div(id='hidden-div', style={'display': 'none'})
    ])
])

@app.callback(
    [Output('container-button', 'children'),
     Output('hidden-div', 'children')],
    Input('button-add-entry', 'n_clicks'),
    State('input-new-entry', 'value'),
    prevent_initial_call=True
)
def add_new_entry(n_clicks, new_entry):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO options (name) VALUES (%s)", (new_entry,))
    connection.commit()
    cursor.close()
    connection.close()
    return f'Entry {new_entry} added!', n_clicks

@app.callback(
    Output('dropdown', 'options'),
    [Input('hidden-div', 'children'),
     Input('button-add-entry', 'n_clicks')]
)
def update_dropdown(trigger, n_clicks):
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    query = "SELECT name FROM options"
    df = pd.read_sql(query, connection)
    options = [{'label': name, 'value': name} for name in df['name']]
    connection.close()
    return options

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

