# Import necessary libraries
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output

# Load the Hotel Reservation dataset from Kaggle
# Replace 'hotel_reservation_data.csv' with the actual filename and path if needed
file_path = r'https://raw.githubusercontent.com/ZaidAlmelhem/Dashboards/main/Distribution%20of%20Review%20Scores%20for%20Mobile%20Apps/1.Hotel%20Reservations_kaggle.csv'
df_hotel_reservation = pd.read_csv(file_path)

# Create a MinMaxScaler object for normalization
scaler = MinMaxScaler()

# Extract the columns to be scaled
columns_to_scale = ['lead_time', 'arrival_year', 'arrival_month', 'arrival_date', 'avg_price_per_room']

# Apply Min-Max scaling to the selected columns
df_hotel_reservation_scaled = df_hotel_reservation.copy()
df_hotel_reservation_scaled[columns_to_scale] = scaler.fit_transform(df_hotel_reservation[columns_to_scale])

# Create a StandardScaler object for standardization
scaler = StandardScaler()

# Columns to be standardized
columns_to_standardize = ['lead_time', 'arrival_year', 'arrival_month', 'arrival_date', 'avg_price_per_room']

# Create a new DataFrame to store the standardized values
df_standardization = df_hotel_reservation.copy()

# Standardize the columns
df_standardization[columns_to_standardize] = scaler.fit_transform(df_hotel_reservation[columns_to_standardize])

# Create the Dash app for visualization
app = Dash(__name__)
server = app.server
# Create the app layout
app.layout = html.Div(
    children=[
        html.H1("Feature Scaling Visualization", style={"text-align": "center"}),
        html.Div("Select a column to visualize its distribution before and after scaling:"),
        dcc.Dropdown(
            id="scaling-column",
            options=[{"label": col, "value": col} for col in columns_to_scale],
            value=columns_to_scale[0],
            style={"width": "50%", "margin": "auto", "color": "black"}
        ),
        html.Div(
            children=[
                dcc.Graph(id="histogram-before-scaling", style={"width": "100%"}),
                dcc.Graph(id="histogram-after-normalization", style={"width": "100%"}),
                dcc.Graph(id="histogram-after-standardization", style={"width": "100%"})
            ],
            style={"display": "flex", "flex-wrap": "wrap", "justify-content": "space-around"}
        )
    ],
    style={"padding": "50px", "background-color": "#303030", "color": "white"}
)

# Custom colors for bars
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Callback to update histograms
@app.callback(
    [Output("histogram-before-scaling", "figure"),
     Output("histogram-after-normalization", "figure"),
     Output("histogram-after-standardization", "figure")],
    [Input("scaling-column", "value")]
)
def update_histograms(selected_column):
    # Create histograms before scaling
    fig_before_scaling = px.histogram(df_hotel_reservation, x=selected_column, title=f"{selected_column.capitalize()} - Before Scaling",
                                      color_discrete_sequence=[bar_colors[0]])

    fig_before_scaling.update_layout(template='plotly_dark', bargap=0.1, bargroupgap=0.1)

    # Create histograms after normalization
    fig_after_normalization = px.histogram(df_hotel_reservation_scaled, x=selected_column, title=f"{selected_column.capitalize()} - After Normalization",
                                          color_discrete_sequence=[bar_colors[1]])

    fig_after_normalization.update_layout(template='plotly_dark', bargap=0.1, bargroupgap=0.1)
    
    # Create histograms after standardization
    fig_after_standardization = px.histogram(df_standardization, x=selected_column, title=f"{selected_column.capitalize()} - After Standardization",
                                            color_discrete_sequence=[bar_colors[2]])

    fig_after_standardization.update_layout(template='plotly_dark', bargap=0.1, bargroupgap=0.1)

    return fig_before_scaling, fig_after_normalization, fig_after_standardization

if __name__ == "__main__":
    app.run_server(debug=True)

