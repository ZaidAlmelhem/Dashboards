import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Sampled dataframe 'sampled_df' containing the required columns
# Replace this with your actual dataframe
# sampled_df = pd.read_csv('path_to_sampled_df.csv')  # Load your data here

sampled_df = pd.read_csv(r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/sampled_df_8_7.csv')

# Create a Dash app
app = dash.Dash(__name__)
server = server.app
# CSS styles
background_colors = {
    'main': '#152737',
    'secondary1': '#1d314a',
    'secondary2': '#0e1826',
}

text_colors = {
    'main': '#a4edb8',
    'secondary1': '#00c6ff',
    'secondary2': '#c7f1d8',
}

styles = {
    'textAlign': 'center',
    'backgroundColor': '#000000',
    'color': '#00c6ff',
    'fontFamily': 'Arial',
    'fontSize': '18px',
    'padding': '20px',
    'margin': '20px',
    'borderRadius': '10px',
    #'boxShadow': '0px 4px 8px rgba(255, 215, 0, 0.5)',
}

# Larger font size for labels
label_style = {'fontSize': '24px', 'fontWeight': 'bold', 'color': text_colors['secondary1']}

# Layout of the app
app.layout = html.Div(style={'maxWidth': '800px', 'margin': 'auto', 'padding': '40px'}, children=[
    html.H1("Sentiment Analysis Dashboard", style={'textAlign': 'center', 'color': text_colors['secondary1'], 'marginBottom': '40px'}),
    
    # Dropdown to select the name of the app
    html.Label("Select the Name of the App:", style={'fontSize': '18px',}),
    dcc.Dropdown(
        id='app-name-dropdown',
        options=[{'label': app_name, 'value': app_name} for app_name in sampled_df['app_name'].unique()],
        value=sampled_df['app_name'].unique()[0]
        
    ),
    
    # Slider to filter the score
    html.Label("Select Score Filter:", style={'fontSize': '18px',}),
    dcc.Slider(
        id='score-filter-slider',
        min=1,
        max=5,
        value=3,
        marks={i: str(i) for i in range(1, 6)},
        step=1,
        className='slider-style',
        updatemode='drag',
    ),
    
    # Placeholder for displaying the reviews and sentiment analysis
    html.Div(id='review-sentiment-container', style={'textAlign': 'left'}),
])

# Create a function to generate a card for each review
def create_review_card(index, row):
    return html.Details([
        html.Summary(f"Review {index}", style={'color': text_colors['secondary1'], 'cursor': 'pointer'}),
        html.Div([
            html.P(f"Review Text: {row['review']}", style={'color': text_colors['main']}),
            html.P(f"Processed Text: {row['processed_text']}", style={'color': text_colors['main']}),
            html.P(f"Score: {row['score']}", style={'color': text_colors['secondary1']}),
            html.P(f"TextBlob Sentiment Score: {row['textblob_sentiment_score']}", style={'color': text_colors['secondary1']}),
            html.P(f"Bert Sentiment Score: {row['bert_sentiment_score']}", style={'color': text_colors['secondary1']}),
            html.P(f"Segmented Bert Sentiment Score: {row['segmented_bert_sentiment_score']}", style={'color': text_colors['secondary1']}),
            html.Hr(),
        ]),
    ], style={**styles, 'border': f'2px solid {text_colors["secondary2"]}', 'margin': '10px'}, id=f"card-{index}")

# Callback to update the review and sentiment analysis display
@app.callback(
    Output('review-sentiment-container', 'children'),
    Input('app-name-dropdown', 'value'),
    Input('score-filter-slider', 'value')
)
def update_review_sentiment(app_name, score_filter):
    filtered_reviews = sampled_df[(sampled_df['app_name'] == app_name) & (sampled_df['score'] == score_filter)]
    
    review_sentiment_html = []
    for index, row in filtered_reviews.iterrows():
        review_sentiment_html.append(create_review_card(index, row))
    
    return review_sentiment_html

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
