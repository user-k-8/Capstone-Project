import pandas as pd

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True),
                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
             
               
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):

    df5= spacex_df.groupby(['Launch Site', 'class'],as_index=False)[['class']].count().rename(columns={'class':'count'})
    df6 = df5.groupby(['Launch Site'],as_index=False)[['count']].sum()
    df5['class'] = df5['count']
    for i in range(8):
        if i%2==0:
            df5['class'][i] = 0
        else:
            df5['class'][i] = 1
    site1 = df5.iloc[0:2, 0:3]
    site2 = df5.iloc[2:4, 0:3]
    site3 = df5.iloc[4:6, 0:3]
    site4 = df5.iloc[6:8, 0:3]

    

    if entered_site == 'ALL':
        fig = px.pie(df6, values='count', 
        names='Launch Site', 
        title= 'Total Success Launches By Site')
        return fig
        
    else:
        d = {'CCAFS LC-40': site1, 
              'VAFB SLC-4E': site4,
               'KSC LC-39A': site3,
             'CCAFS SLC-40': site2}
        # return the outcomes piechart for a selected site
        fig = px.pie(d[str(entered_site)], values='count', names='class', 
        title='Total Success Launches for site ' + entered_site )
        return fig  

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


    
# Run the app
if __name__ == '__main__':
    app.run_server()

