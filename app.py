#!/usr/bin/env python
# coding: utf-8

# <div><p><!-- react-text: 7004 -->The <!-- /react-text -->first part<!-- /react-text --><!-- react-text: 7007 --> of this tutorial
# covered the <!-- /react-text --><code>layout</code><!-- react-text: 7009 --> of Dash apps. The <!-- /react-text --><code>layout</code><!-- react-text: 7011 --> of a Dash app
# describes what the app looks like.
# It is a hierarchical tree of components.
# The <!-- /react-text --><code>dash_html_components</code><!-- react-text: 7013 --> library provides classes for all of the HTML
# tags and the keyword arguments describe the HTML attributes like <!-- /react-text --><code>style</code><!-- react-text: 7015 -->,
# <!-- /react-text --><code>className</code><!-- react-text: 7017 -->, and <!-- /react-text --><code>id</code><!-- react-text: 7019 -->. The <!-- /react-text --><code>dash_core_components</code><!-- react-text: 7021 --> library
# generates higher-level components like controls and graphs.<!-- /react-text --></p><p><!-- react-text: 7023 -->The second part of the tutorial describes how to make your
# Dash apps interactive.<!-- /react-text --></p><p><!-- react-text: 7025 -->Let's get started with a simple example.<!-- /react-text --></p></div>

# In[1]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type="text"),
    html.Div(id='my-div')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server()


# <div><p><!-- react-text: 7105 -->Try typing in the text box. The children of the output component updates
# right away. Let's break down what's happening here:<!-- /react-text --></p><ol><li><!-- react-text: 7108 -->The "inputs" and "outputs" of our application interface are described
# declaratively through the <!-- /react-text --><code>app.callback</code><!-- react-text: 7110 --> decorator.<!-- /react-text --></li><li><!-- react-text: 7112 -->In Dash, the inputs and outputs of our application are simply the
# properties of a particular component. In this example,
# our input is the "<!-- /react-text --><code>value</code><!-- react-text: 7114 -->" property of the component that has the ID
# "<!-- /react-text --><code>my-id</code><!-- react-text: 7116 -->". Our output is the "<!-- /react-text --><code>children</code><!-- react-text: 7118 -->" property of the
# component with the ID "<!-- /react-text --><code>my-div</code><!-- react-text: 7120 -->".<!-- /react-text --></li><li><!-- react-text: 7122 -->Whenever an input property changes, the function that the
# callback decorator wraps will get called automatically.
# Dash provides the function with the new value of the input property as
# an input argument and Dash updates the property of the output component
# with whatever was returned by the function.<!-- /react-text --></li><li><!-- react-text: 7130 -->Don't confuse the <!-- /react-text --><code>dash.dependencies.Input</code><!-- react-text: 7132 --> object from the
# <!-- /react-text --><code>dash_core_components.Input</code><!-- react-text: 7134 --> object. The former is just used in these
# callbacks and the latter is an actual component.<!-- /react-text --></li><li><!-- react-text: 7136 -->Notice how we don't set a value for the <!-- /react-text --><code>children</code><!-- react-text: 7138 --> property of the
# <!-- /react-text --><code>my-div</code><!-- react-text: 7140 --> component in the <!-- /react-text --><code>layout</code><!-- react-text: 7142 -->. When the Dash app starts, it
# automatically calls all of the callbacks with the initial values of the
# input components in order to populate the initial state of the output
# components. In this example, if you specified something like
# <!-- /react-text --><code>html.Div(id='my-div', children='Hello world')</code><!-- react-text: 7144 -->, it would get overwritten
# when the app starts.<!-- /react-text --></li></ol><p><!-- react-text: 7148 -->Remember how every component was described entirely through its set of
# keyword arguments? Those properties are important now.
# With Dash interactivity, we can dynamically update any of those properties
# through a callback function. Frequently we'll update the <!-- /react-text --><code>children</code><!-- react-text: 7150 --> of a
# component to display new text or the <!-- /react-text --><code>figure</code><!-- react-text: 7152 --> of a <!-- /react-text --><code>dcc.Graph</code><!-- react-text: 7154 --> component
# to display new data, but we could also update the <!-- /react-text --><code>style</code><!-- react-text: 7156 --> of a component or
# even the available <!-- /react-text --><code>options</code><!-- react-text: 7158 --> of a <!-- /react-text --><code>dcc.Dropdown</code><!-- react-text: 7160 --> component!<!-- /react-text --></p><hr><p><!-- react-text: 7163 -->Let's take a look at another example where a <!-- /react-text --><code>dcc.Slider</code><!-- react-text: 7165 --> updates a
# <!-- /react-text --><code>dcc.Graph</code><!-- react-text: 7167 -->.<!-- /react-text --></p></div>

# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 7416 -->In this example, the <!-- /react-text --><code>"value"</code><!-- react-text: 7418 --> property of the <!-- /react-text --><code>Slider</code><!-- react-text: 7420 --> is the input of the app
# and the output of the app is the <!-- /react-text --><code>"figure"</code><!-- react-text: 7422 --> property of the <!-- /react-text --><code>Graph</code><!-- react-text: 7424 -->.
# Whenever the <!-- /react-text --><code>value</code><!-- react-text: 7426 --> of the <!-- /react-text --><code>Slider</code><!-- react-text: 7428 --> changes, Dash calls the callback
# function <!-- /react-text --><code>update_figure</code><!-- react-text: 7430 --> with the new value. The function filters the
# dataframe with this new value, constructs a <!-- /react-text --><code>figure</code><!-- react-text: 7432 --> object,
# and returns it to the Dash application.<!-- /react-text --></p><p><!-- react-text: 7434 -->There are a few nice patterns in this example:<!-- /react-text --></p><ol><li><!-- react-text: 7437 -->We're using the <!-- /react-text --><a href="http://pandas.pydata.org/"><!-- react-text: 7439 -->Pandas<!-- /react-text --></a><!-- react-text: 7440 --> library for importing
# and filtering datasets in memory.<!-- /react-text --></li><li><!-- react-text: 7442 -->We load our dataframe at the start of the app: <!-- /react-text --><code>df = pd.read_csv('...')</code><!-- react-text: 7444 -->.
# This dataframe <!-- /react-text --><code>df</code><!-- react-text: 7446 --> is in the global state of the app and can be
# read inside the callback functions.<!-- /react-text --></li><li><!-- react-text: 7448 -->Loading data into memory can be expensive. By loading querying data at
# the start of the app instead of inside the callback functions, we ensure
# that this operation is only done when the app server starts. When a user
# visits the app or interacts with the app, that data (the <!-- /react-text --><code>df</code><!-- react-text: 7450 -->)
# is already in memory.
# If possible, expensive initialization (like downloading or querying data)
# should be done in the global scope of the app instead of within the
# callback functions.<!-- /react-text --></li><li><!-- react-text: 7452 -->The callback does not modify the original data, it just creates copies
# of the dataframe by filtered through pandas filters.
# This is important: <!-- /react-text --><em><!-- react-text: 7454 -->your callbacks should never mutate variables
# outside of their scope<!-- /react-text --></em><!-- react-text: 7455 -->. If your callbacks modify global state, then one
# user's session might affect the next user's session and when the app is
# deployed on multiple processes or threads, those modifications will not
# be shared across sessions.<!-- /react-text --></li></ol><h4>Multiple inputs</h4><p><!-- react-text: 7458 -->In Dash any "<!-- /react-text --><code>Output</code><!-- react-text: 7460 -->" can have multiple "<!-- /react-text --><code>Input</code><!-- react-text: 7462 -->" components.
# Here's a simple example that binds 5 Inputs
# (the <!-- /react-text --><code>value</code><!-- react-text: 7464 --> property of 2 <!-- /react-text --><code>Dropdown</code><!-- react-text: 7466 --> components, 2 <!-- /react-text --><code>RadioItems</code><!-- react-text: 7468 --> components,
# and 1 <!-- /react-text --><code>Slider</code><!-- react-text: 7470 --> component) to 1 Output component
# (the <!-- /react-text --><code>figure</code><!-- react-text: 7472 --> property of the <!-- /react-text --><code>Graph</code><!-- react-text: 7474 --> component).
# Notice how the <!-- /react-text --><code>app.callback</code><!-- react-text: 7476 --> lists all 5 <!-- /react-text --><code>dash.dependencies.Input</code><!-- react-text: 7478 --> inside
# a list in the second argument.<!-- /react-text --></p></div>

# In[3]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 7938 -->In this example, the <!-- /react-text --><code>update_graph</code><!-- react-text: 7940 --> function gets called whenever the
# <!-- /react-text --><code>value</code><!-- react-text: 7942 --> property of the <!-- /react-text --><code>Dropdown</code><!-- react-text: 7944 -->, <!-- /react-text --><code>Slider</code><!-- react-text: 7946 -->, or <!-- /react-text --><code>RadioItems</code><!-- react-text: 7948 --> components
# change.<!-- /react-text --></p><p><!-- react-text: 7950 -->The input arguments of the <!-- /react-text --><code>update_graph</code><!-- react-text: 7952 --> function are the new or current
# value of the each of the <!-- /react-text --><code>Input</code><!-- react-text: 7954 --> properties, in the order that they were
# specified.<!-- /react-text --></p><p><!-- react-text: 7956 -->Even though only a single <!-- /react-text --><code>Input</code><!-- react-text: 7958 --> changes at a time (a user can only change
# the value of a single Dropdown in a given moment), Dash collects the current
# state of all of the specified <!-- /react-text --><code>Input</code><!-- react-text: 7960 --> properties and passes them into your
# function for you. Your callback functions are always guarenteed to be passed
# the representative state of the app.<!-- /react-text --></p><p><!-- react-text: 7962 -->Let's extend our example to include multiple outputs.<!-- /react-text --></p><h4>Multiple Outputs</h4><p><!-- react-text: 7965 -->Each Dash callback function can only update a single Output property.
# To update multiple Outputs, just write multiple functions.<!-- /react-text --></p></div>

# In[4]:


import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash('')
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    dcc.RadioItems(
        id='dropdown-a',
        options=[{'label': i, 'value': i} for i in ['Canada', 'USA', 'Mexico']],
        value='Canada'
    ),
    html.Div(id='output-a'),

    dcc.RadioItems(
        id='dropdown-b',
        options=[{'label': i, 'value': i} for i in ['MTL', 'NYC', 'SF']],
        value='MTL'
    ),
    html.Div(id='output-b')

])

@app.callback(
    dash.dependencies.Output('output-a', 'children'),
    [dash.dependencies.Input('dropdown-a', 'value')])
def callback_a(dropdown_value):
    return 'You\'ve selected "{}"'.format(dropdown_value)

@app.callback(
    dash.dependencies.Output('output-b', 'children'),
    [dash.dependencies.Input('dropdown-b', 'value')])
def callback_b(dropdown_value):
    return 'You\'ve selected "{}"'.format(dropdown_value)

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 8140 -->You can also chain outputs and inputs together: the output of one callback
# function could be the input of another callback function.<!-- /react-text --></p><p><!-- react-text: 8142 -->This pattern can be used to create dynamic UIs where one input component
# updates the available options of the next input component.
# Here's a simple example.<!-- /react-text --></p></div>

# In[5]:


# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}
app.layout = html.Div([
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-dropdown'),

    html.Hr(),

    html.Div(id='display-selected-values')
])

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'options'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'value'),
    [dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value'),
     dash.dependencies.Input('cities-dropdown', 'value')])
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )

if __name__ == '__main__':
    app.run_server()


# <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
# 
# [http://localhost:8050](http://localhost:8050)
# 
# Press  <i class="fa fa-stop"></i>  in the tool bar before execute the next cell

# <div><p><!-- react-text: 8352 -->The first callback updates the available options in the second <!-- /react-text --><code>RadioItems</code><!-- react-text: 8354 -->
# component based off of the selected value in the first <!-- /react-text --><code>RadioItems</code><!-- react-text: 8356 --> component.<!-- /react-text --></p><p><!-- react-text: 8358 -->The second callback sets an initial value when the <!-- /react-text --><code>options</code><!-- react-text: 8360 --> property changes:
# it sets it to the first value in that <!-- /react-text --><code>options</code><!-- react-text: 8362 --> array.<!-- /react-text --></p><p><!-- react-text: 8364 -->The final callback displays the selected <!-- /react-text --><code>value</code><!-- react-text: 8366 --> of each component.
# If you change the <!-- /react-text --><code>value</code><!-- react-text: 8368 --> of the countries <!-- /react-text --><code>RadioItems</code><!-- react-text: 8370 --> component, Dash
# will wait until the <!-- /react-text --><code>value</code><!-- react-text: 8372 --> of the cities component is updated
# before calling the final callback. This prevents your callbacks from being
# called with inconsistent state like with <!-- /react-text --><code>"USA"</code><!-- react-text: 8374 --> and <!-- /react-text --><code>"Montréal"</code><!-- react-text: 8376 -->.<!-- /react-text --></p></div>

# <div><h3>Summary</h3><p><!-- react-text: 8380 -->We've covered the fundamentals of callbacks in Dash.
# Dash apps are built off of a set
# of simple but powerful principles: declarative UIs that are customizable
# through reactive and functional Python callbacks.
# Every element attribute of the declarative components can be updated through
# a callback and a subset of the attributes, like the <!-- /react-text --><code>value</code><!-- react-text: 8382 --> properties of
# the <!-- /react-text --><code>dcc.Dropdown</code><!-- react-text: 8384 -->, are editable by the user in the interface.<!-- /react-text --></p><hr></div>

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# In[ ]:


#3 input 1 output
#country and indicator 
#Div is the container
#eurostat  view the table   add all the indicators    download--csv
#delete content of Euro-combined contents in python
#the data has three kinds of unit, filter by the units
#: is the missing values

