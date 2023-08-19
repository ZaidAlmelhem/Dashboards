import pandas as pd
import plotly.graph_objects as go
import textwrap
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Create Dash app
app = dash.Dash(__name__)
server = app.server
# Sorting the data in descending order based on thumbs up count
df_reviews_sorted = df_reviews.sort_values(by='thumbs_up_count', ascending=False)

# Create the dropdown options for app names
app_names = df_reviews['app_name'].unique()

# Create the layout for the app
app.layout = html.Div([
    html.H1("Top 20 Reviews with the Most Thumbs Up"),
    dcc.Dropdown(
        id='app-dropdown',
        options=[{'label': app_name, 'value': app_name} for app_name in app_names],
        value=app_names[0]
    ),
    dcc.Graph(id='thumbs-up-bar-plot')
])

# Define callback to update the bar plot based on the selected app name
@app.callback(
    Output('thumbs-up-bar-plot', 'figure'),
    [Input('app-dropdown', 'value')]
)
def update_bar_plot(selected_app):
    # Filter the data for the selected app
    filtered_reviews = df_reviews[df_reviews['app_name'] == selected_app].sort_values(by='thumbs_up_count', ascending=False).head(40).reset_index(drop = True)

    # Create the interactive bar plot
    fig = go.Figure()

    # Function to wrap the review text every 20 words
    def wrap_text(text):
        return '<br>'.join(textwrap.wrap(text, width=80))

    # Function to format the hover text with HTML to make text bigger
    def format_hover_text(review, app_name, thumbs_up_count, score,date):
        review_text = f"<b><span style='font-size: 14px;'>Review:</span></b><br>{wrap_text(review)}"
        app_text = f"<b><span style='font-size: 14px;'>App:</span></b> {app_name}"
        thumbs_up_text = f"<b><span style='font-size: 14px;'>Thumbs Up Count:</span></b> {thumbs_up_count}"
        score_text = f"<b><span style='font-size: 14px;'>Score:</span></b> {score}"
        date= f"<b><span style='font-size: 14px;'>Date:</span></b> {date}"
        return f"{app_text}<br>{thumbs_up_text}<br>{score_text}<br>{review_text}<br>{date}"

    fig.add_trace(go.Bar(
        x=filtered_reviews.index,
        y=filtered_reviews['thumbs_up_count'],
        hovertext=filtered_reviews.apply(lambda row: format_hover_text(row['review'], row['app_name'], row['thumbs_up_count'], row['score'], row['date']), axis=1),
        hoverinfo='text',
        marker_color='#FFD700'  # Gold color for the bars
    ))

    fig.update_layout(
        title=f'Top 40 Reviews with the Most Thumbs Up for {selected_app}',
        xaxis_title='Review Index',
        yaxis_title='Thumbs Up Count',
        xaxis_tickangle=-45,
        showlegend=False,
        plot_bgcolor='#152737',  # Dark background
        paper_bgcolor='#152737',  # Dark background
        font=dict(color='#a4edb8'),  # Light text color
        height=500,
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
