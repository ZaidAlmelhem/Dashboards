import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Assuming you have already loaded the dataset into df_reviews DataFrame

df_reviews = pd.read_csv(r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/google_play_store_reviews.csv')

# Create a Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout of the app
app.layout = html.Div([
    html.H1("Distribution of Review Scores for Mobile Apps"),
    
    dcc.Dropdown(
        id='app-dropdown',
        options=[{'label': app_name, 'value': app_name} for app_name in df_reviews['app_name'].unique()],
        value=df_reviews['app_name'].unique()[0],
        style={'width': '50%'}
    ),
    
    dcc.Graph(id='score-histogram'),
])

# Define the callback to update the histogram based on the selected app_name
@app.callback(
    Output('score-histogram', 'figure'),
    [Input('app-dropdown', 'value')]
)
def update_histogram(app_name):
    filtered_data = df_reviews[df_reviews['app_name'] == app_name]
    fig = px.histogram(filtered_data, x='score', nbins=5, title=f"Distribution of Review Scores for {app_name}",
                       labels={'score': 'Review Score', 'count': 'Frequency'},
                       category_orders={'score': sorted(filtered_data['score'].unique())})
    fig.update_xaxes(type='category', categoryorder='category ascending', tickvals=[1, 2, 3, 4, 5],
                     ticktext=['★', '★★', '★★★', '★★★★', '★★★★★'])
    fig.update_layout(showlegend=False, height=500, template="plotly_dark", )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
