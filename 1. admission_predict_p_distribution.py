import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from ipywidgets import interact
import pandas as pd


# Create a Dash app instance
app = dash.Dash(__name__)

# Load the dataset:
addmision_df = pd.read_csv(r"C:\Users\User\Desktop\GitHub-projects\projects\Data-Dives-Projects-Unleashed\Notebooks\course1\Admission_Predict_cleaned.csv")

# Layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': col, 'value': col} for col in addmision_df.columns.tolist()],
        value=addmision_df.columns.tolist()[0]
    ),
    dcc.Graph(id='histogram-plot')
])

# Define a callback to update the histogram plot
@app.callback(
    Output('histogram-plot', 'figure'),
    [Input('column-dropdown', 'value')]
)
def update_histogram(column):
    # Create a Figure object
    fig = go.Figure()

    # Plot the histogram using Plotly with a beautiful color palette
    fig.add_trace(go.Histogram(x=addmision_df[column], marker=dict(color='turquoise')))

    # Update layout
    fig.update_layout(
        title=f"Distribution of {column} in Admission Data",
        xaxis_title=column,
        yaxis_title="Frequency",
        bargap=0.1,
        bargroupgap=0.2,
        template="plotly_dark"  # Using a dark template for an appealing look
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
