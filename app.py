import streamlit as st
import requests
import datetime
import pandas as pd
import random

# A brief introduction to the app.
st.title("💸2025 Prices... 🚕1978 Cars...")

# The URL for the API. You will need to replace this with your actual URL.
# This variable is clearly marked for the user to update.
API_URL = 'https://taxifare-505391779697.europe-southwest1.run.app/predict'

# The image of the yellow taxi
st.image("https://i.postimg.cc/XJR87PR3/17828228261-3cf73de867-b.jpg")

# Initialize session state for coordinates if they don't exist
if 'pickup_latitude' not in st.session_state:
    st.session_state.pickup_latitude = 40.757139
    st.session_state.pickup_longitude = -73.985655
if 'dropoff_latitude' not in st.session_state:
    st.session_state.dropoff_latitude = 40.761421
    st.session_state.dropoff_longitude = -73.987795

# Function to generate random NYC-like coordinates and update session state
def randomize_coordinates():
    st.session_state.pickup_latitude = random.uniform(40.7, 40.8)
    st.session_state.pickup_longitude = random.uniform(-74.0, -73.9)
    st.session_state.dropoff_latitude = random.uniform(40.7, 40.8)
    st.session_state.dropoff_longitude = random.uniform(-74.0, -73.9)

# Create a form to gather all the user inputs.
with st.form(key='fare_form'):
    # A button to randomize coordinates
    st.button("Randomize Coordinates", on_click=randomize_coordinates)

    # Let's get the date and time.
    # The default value is set to the current date and time.
    date = st.date_input("Date of the ride", value=datetime.date.today())
    time = st.time_input("Time of the ride", value=datetime.time(12, 0))

    # Get the pickup and dropoff coordinates using number inputs.
    # The step size is set for more precise input.
    st.markdown("#### Pickup and Dropoff Coordinates")
    col1, col2 = st.columns(2)
    with col1:
        # Connect input values to session state
        pickup_longitude = st.number_input("Pickup Longitude", value=st.session_state.pickup_longitude, format="%.6f", step=0.000001)
        pickup_latitude = st.number_input("Pickup Latitude", value=st.session_state.pickup_latitude, format="%.6f", step=0.000001)
    with col2:
        dropoff_longitude = st.number_input("Dropoff Longitude", value=st.session_state.dropoff_longitude, format="%.6f", step=0.000001)
        dropoff_latitude = st.number_input("Dropoff Latitude", value=st.session_state.dropoff_latitude, format="%.6f", step=0.000001)

    # Get the passenger count.
    passenger_count = st.slider(
        "Number of Passengers",
        min_value=1,
        max_value=8,
        value=1
    )

    # A button to submit the form.
    submit_button = st.form_submit_button(label='Get Predicted Fare')

# Logic to handle the form submission.
if submit_button:
    # Check if the API URL has been set.
    if API_URL == 'http://your-api-url.com/predict':
        st.error("Please enter your API URL in the code to get a prediction.")
    else:
        # Construct the full datetime string.
        pickup_datetime = f"{date} {time}"

        # Create a dictionary with the parameters to be sent to the API.
        params = {
            'pickup_datetime': pickup_datetime,
            'pickup_longitude': pickup_longitude,
            'pickup_latitude': pickup_latitude,
            'dropoff_longitude': dropoff_longitude,
            'dropoff_latitude': dropoff_latitude,
            'passenger_count': int(passenger_count)
        }

        # Display a spinner while waiting for the API response.
        with st.spinner("Calling API for prediction..."):
            try:
                # Make the GET request to the API.
                response = requests.get(API_URL, params=params, timeout=10)
                # Raise an exception for bad status codes (e.g., 404, 500).
                response.raise_for_status()

                # Get the JSON response.
                prediction = response.json()

                # Check if the 'fare' key is in the response.
                if 'fare' in prediction:
                    fare = round(prediction['fare'], 2)
                    st.success(f"### 💰 Predicted Fare: ${fare}")

                    # Create a DataFrame with the pickup and dropoff points for the map
                    map_data = pd.DataFrame(
                        [
                            {"lat": pickup_latitude, "lon": pickup_longitude},
                            {"lat": dropoff_latitude, "lon": dropoff_longitude}
                        ]
                    )

                    # Display the map showing the two points
                    st.map(map_data, zoom=12)
                else:
                    # Provide a more detailed error message with the full API response
                    st.error(f"Error: API response did not contain a 'fare' key. Full response: {prediction}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error calling the API: {e}")
            except ValueError as e:
                st.error(f"Error parsing API response: {e}")

