import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
from wordcloud import WordCloud
from io import BytesIO

# Sampled dataframe 'sampled_df' containing the required columns
# Replace this with your actual dataframe
# sampled_df = pd.read_csv('path_to_sampled_df.csv')  # Load your data here

#sampled_df = pd.read_csv(r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/sampled_bertopic_df.csv')
  
# Create a Dash app
app = dash.Dash(__name__)
server = app.server
# Layout of the app
app.layout = html.Div([
    html.H1("Word Cloud Dashboard", style = {'text-align': 'center'}),
    
    # Dropdown to select the topic
    dcc.Dropdown(
        id='topic-dropdown',
        options=[{'label': 'Topic ' + str(topic), 'value': topic} for topic in sampled_df['topic'].unique()],
        value=sampled_df['topic'].unique()[0]
    ),
    
    # Placeholder for displaying the word cloud image
    html.Div([
        html.Img(id='word-cloud-image', style={'height': '600px', 'width': '1200px'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100vh'}),
])

# Create a function to generate word cloud image for a specific topic
def generate_word_cloud(topic):
    reviews_text = ' '.join(sampled_df[sampled_df['topic'] == topic]['review'])
    wordcloud = WordCloud(width=1200, height=600, background_color='white').generate(reviews_text)
    return wordcloud

# Callback to update the word cloud image
@app.callback(
    Output('word-cloud-image', 'src'),
    Input('topic-dropdown', 'value')
)
def update_word_cloud(topic):
    word_cloud_img = generate_word_cloud(topic)
    word_cloud_img_bytes = BytesIO()
    word_cloud_img.to_image().save(word_cloud_img_bytes, format='PNG')
    word_cloud_img_base64 = base64.b64encode(word_cloud_img_bytes.getvalue()).decode('utf-8')
    src_attr = f'data:image/png;base64,{word_cloud_img_base64}'
    return src_attr

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
