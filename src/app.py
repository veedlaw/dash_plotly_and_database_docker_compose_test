import dash
from dash import dcc, html
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import os

db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


# Connect to MySQL database
connection = pymysql.connect(host='mysql',
                             user='user',
                             password='password',
                             database='mydb')

# Fetch data from database
query = "SELECT name FROM options"
df = pd.read_sql(query, connection)

options = [{'label': name, 'value': name} for name in df['name']]

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=options,
        value=options[0]['value']
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

