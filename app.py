#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.plotly as py

r = pd.read_csv('nama_10_gdp_1_Data.csv')
r.drop(labels='Flag and Footnotes',axis=1,inplace=True)
r=r[~r['Value'].str.contains(':')]
df=r[~r['GEO'].str.contains('Euro')]


# In[2]:


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators1 = df['NA_ITEM'].unique()
available_indicators2 = df['UNIT'].unique()
available_indicators3 = df['NA_ITEM'].unique()
available_indicators4 = df['GEO'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis_column',
                    options=[{'label': u, 'value': u} for u in available_indicators1],
                    value='Value added, gross')],
                style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis_column',
                    options=[{'label': n, 'value': n} for n in available_indicators2],
                    value='Chain linked volumes, index 2010=100')],
                style={'width': '48%', 'float': 'right', 'display': 'inline-block'})]),

        dcc.Graph(id='indicator-graphic1'),

        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )
    ],
        style={'width': '100%', 'padding': '0px 20px 20px 20px'}),
    
    html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(id='item',
                    options=[{'label': u, 'value': u} for u in available_indicators3],
                    value='Gross domestic product at market prices'),
                dcc.RadioItems(
                    id='unit',
                    options=[{'label': i, 'value': i} for i in df['UNIT'].unique()],
                    value='Chain linked volumes, index 2010=100',
                    labelStyle={'display': 'inline-block'})],
                style={'width': '48%', 'display': 'inline-block'}),
        
            html.Div([
                dcc.Dropdown(
                    id='GEO',
                    options=[{'label': n, 'value': n} for n in available_indicators4],
                    value='Belgium')],
                style={'width': '48%', 'float': 'right', 'display': 'inline-block'})]),

        dcc.Graph(id='indicator-graphic2')
    ])
])
    

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    [dash.dependencies.Input('xaxis_column', 'value'),
     dash.dependencies.Input('yaxis_column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])  
def update_graph(xaxis_column_name, 
                 yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM']==xaxis_column_name]['Value'],
            y=dff[dff['UNIT'] == yaxis_column_name]['Value'],
            text=dff[(dff['NA_ITEM'] == xaxis_column_name) & (dff['UNIT'] == yaxis_column_name)]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 50, 'b': 50, 't': 50, 'r': 10},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('item', 'value'),
     dash.dependencies.Input('unit', 'value'),
     dash.dependencies.Input('GEO', 'value')])

def update_graph(item_name, unit_name,
                GEO_name):
    year=df['TIME'].unique()
    return {
        'data': [go.Scatter(
            x=year,
            y=df[(df['NA_ITEM']==item_name)&(df['UNIT']==unit_name)&(df['GEO']==GEO_name)]['Value'],
            
            mode='markers+lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 2.0, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title=GEO_name +"  "+ item_name,
            xaxis={'title':'Year'},
            yaxis={'title':unit_name},
            margin={'l': 100, 'b': 100, 't': 100, 'r': 100},
            hovermode='closest'
        )
    }
    
if __name__ == '__main__':
    app.run_server()


# In[ ]:




