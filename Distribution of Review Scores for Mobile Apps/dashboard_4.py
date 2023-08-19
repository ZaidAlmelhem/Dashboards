import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Sampled dataframe 'sampled_df' containing the required columns
# Replace this with your actual dataframe
# sampled_df = pd.read_csv('path_to_sampled_df.csv')  # Load your data here

sampled df = pd.read_csv(r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/sampled_df_8_7.csv')

# Create a Dash app
app = dash.Dash(__name__)
server = server.app

# Layout of the app
app.layout = html.Div([
    html.H1("Sentiment Analysis Dashboard"),
    
    # Dropdown to select the name of the app
    html.Label("Select the Name of the App:"),
    dcc.Dropdown(
        id='app-name-dropdown',
        options=[{'label': app_name, 'value': app_name} for app_name in sampled_df['app_name'].unique()],
        value=sampled_df['app_name'].unique()[0],
    ),
    
    # Slider to filter the score
    html.Label("Select Score Filter:"),
    dcc.Slider(
        id='score-filter-slider',
        min=1,
        max=5,
        value=3,
        marks={i: str(i) for i in range(1, 6)},
        step=1
    ),
    
    # Placeholder for displaying the reviews and sentiment analysis
    html.Div(id='review-sentiment-container'),
])

# Callback to update the review and sentiment analysis display
@app.callback(
    Output('review-sentiment-container', 'children'),
    Input('app-name-dropdown', 'value'),
    Input('score-filter-slider', 'value')
)
def update_review_sentiment(app_name, score_filter):
    filtered_reviews = sampled_df[(sampled_df['app_name'] == app_name) & (sampled_df['score'] == score_filter)]
    
    review_sentiment_html = []
    for _, row in filtered_reviews.iterrows():
        review_sentiment_html.append(html.Div([
            html.H3(f"Review {row.name}"),
            html.P(f"Review Text: {row['review']}"),
            html.P(f"Processed Text: {row['processed_text']}"),
            html.P(f"Score: {row['score']}"),
            html.P(f"TextBlob Sentiment Score: {row['textblob_sentiment_score']}"),
            html.P(f"Bert Sentiment Score: {row['bert_sentiment_score']}"),
            html.P(f"Segmented Bert Sentiment Score: {row['segmented_bert_sentiment_score']}"),
            html.Hr(),
        ]))
    
    return review_sentiment_html

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
