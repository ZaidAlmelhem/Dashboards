import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
from lime import lime_tabular
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

# Load the saved model from the file
filename = r'final_model_NAS.pkl'
final_model = joblib.load(filename)
df_hotel_reservation_scaled = pd.read_csv(r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/df_hotel_reservation_scaled.csv')

# Specify the features (X) and target (y) columns
features = df_hotel_reservation_scaled.drop('booking_status', axis=1)
target = df_hotel_reservation_scaled['booking_status']

# Split the data into training and testing sets (80% for training, 20% for testing)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Convert Pandas DataFrame to numpy arrays
X_train_array = X_train.values
X_test_array = X_test.values

# Get the feature names from the DataFrame columns
feature_names = X_train.columns

# Generate local explanations using LIME
explainer = lime_tabular.LimeTabularExplainer(X_train_array, feature_names=feature_names, class_names=['canceled', 'not canceled'], discretize_continuous=True)

# Create the Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout of the app with dark background color
app.layout = html.Div(style={'backgroundColor': '#222222', 'color': 'white', 'padding': '20px'}, children=[
    # Input field to allow the user to choose the data instance by selecting the index
    dcc.Input(id='data-index', type='number', value=0, min=0, max=len(X_test)-1, step=1, style={'margin-bottom': '20px'}),
    
    # Graph to display the local prediction plot
    dcc.Graph(id='local-prediction-plot'),
    
    # Graph to display the model's correct and incorrect predictions
    dcc.Graph(id='prediction-counts-plot'),
    
    # Graph to display counts of incorrect predictions in each class
    dcc.Graph(id='incorrect-predictions-plot')
])

# Function to generate the LIME explanation and plot
def generate_local_prediction_plot(data_index):
    # Generate local explanations using LIME
    data_point_of_interest = X_test_array[data_index]
    explanation = explainer.explain_instance(data_point_of_interest, final_model.predict_proba, num_features=len(feature_names))

    # Get the predicted class and probabilities
    probs = explanation.predict_proba
    classes = ['canceled', 'not canceled']
    class_names = ['Canceled', 'Not Canceled']
    correct_choice = class_names[np.argmax(probs)]
    
    # Create the Local Prediction Plot using plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=class_names, y=probs, marker_color=['red', 'blue'], hoverinfo='text',
                         text=[f"Class: {class_names[i]}<br>Probability: {probs[i]:.4f}" for i in range(len(probs))],
                         name='Local Prediction'))

    fig.update_layout(title='Local Prediction Plot', xaxis_title='Class', yaxis_title='Probability',
                      legend=dict(x=0, y=1.1), plot_bgcolor='#222222', paper_bgcolor='#222222', font_color='white',
                      annotations=[dict(text=f"Correct Choice: {correct_choice}", x=0.5, y=-0.15, showarrow=False)])
    
    return fig

# Callback to update the plot based on the selected data index
@app.callback(
    Output('local-prediction-plot', 'figure'),
    [Input('data-index', 'value')]
)
def update_local_prediction_plot(data_index):
    return generate_local_prediction_plot(data_index)

# Function to generate the model's correct and incorrect predictions count
def generate_prediction_counts_plot():
    # Make predictions on the entire test set
    predictions = final_model.predict(X_test)
    correct_counts = np.sum(predictions == y_test)
    incorrect_counts = np.sum(predictions != y_test)
    
    # Create the Prediction Counts Plot using plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Correct Predictions', 'Incorrect Predictions'], y=[correct_counts, incorrect_counts],
                         marker_color=['green', 'red'], hoverinfo='text',
                         text=[f"Counts: {correct_counts}", f"Counts: {incorrect_counts}"],
                         name='Prediction Counts'))
    
    fig.update_layout(title='Model Prediction Counts', xaxis_title='Prediction', yaxis_title='Counts',
                      plot_bgcolor='#222222', paper_bgcolor='#222222', font_color='white')
    
    return fig

# Callback to update the prediction counts plot
@app.callback(
    Output('prediction-counts-plot', 'figure'),
    [Input('data-index', 'value')]
)
def update_prediction_counts_plot(data_index):
    return generate_prediction_counts_plot()

# Function to generate counts of incorrect predictions in each class
def generate_incorrect_predictions_plot():
    # Make predictions on the entire test set
    predictions = final_model.predict(X_test)
    
    # Count the number of incorrect predictions in each class
    class_names = ['Canceled', 'Not Canceled']
    incorrect_counts = [np.sum((predictions != y_test) & (y_test == i)) for i in range(len(class_names))]
    
    # Create the Incorrect Predictions Plot using plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=class_names, y=incorrect_counts, marker_color='red', hoverinfo='text',
                         text=[f"Class: {class_names[i]}<br>Counts: {incorrect_counts[i]}" for i in range(len(incorrect_counts))],
                         name='Incorrect Predictions'))

    fig.update_layout(title='Incorrect Predictions Counts', xaxis_title='Class', yaxis_title='Counts',
                      plot_bgcolor='#222222', paper_bgcolor='#222222', font_color='white')
    
    return fig

# Callback to update the incorrect predictions plot
@app.callback(
    Output('incorrect-predictions-plot', 'figure'),
    [Input('data-index', 'value')]
)
def update_incorrect_predictions_plot(data_index):
    return generate_incorrect_predictions_plot()

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
