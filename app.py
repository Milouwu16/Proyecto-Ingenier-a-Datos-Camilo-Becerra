import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import psycopg2

# Conexión a la base de datos PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",  # Nombre del host (o dirección IP) de tu servidor PostgreSQL
        database="Proyecto",
        user="postgres",
        password="1606"
    )
    return conn

# Consulta de datos de todas las tablas
def query_all_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    data = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        data[table_name] = {
            'description': cursor.description,
            'data': rows
        }
    cursor.close()
    conn.close()
    return data

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Datos de las Tablas"),
    dcc.Dropdown(
        id='table-dropdown',
        options=[{'label': table, 'value': table} for table in query_all_tables().keys()],
        value=None
    ),
    html.Div(id='table-data')
])

# Callback para mostrar los datos de la tabla seleccionada
@app.callback(
    Output('table-data', 'children'),
    [Input('table-dropdown', 'value')]
)
def display_table_data(table_name):
    if table_name is None:
        return ''
    table_data = query_all_tables()[table_name]
    description = table_data['description']
    data = table_data['data']
    return html.Table(
        # Cabecera de la tabla
        [html.Tr([html.Th(col[0]) for col in description])] +
        # Filas de la tabla
        [html.Tr([html.Td(cell) for cell in row]) for row in data]
    )

if __name__ == '__main__':
    app.run_server(debug=True, port ='8085')

