import streamlit as st
import requests
import datetime
import pandas as pd

# A brief introduction to the app.
st.title("💸2025 Prices... 🚕1978 Cars...")

# The URL for the API. You will need to replace this with your actual URL.
# This variable is clearly marked for the user to update.
API_URL = 'https://taxifare-505391779697.europe-southwest1.run.app/predict'

# The image of the yellow taxi
st.image("https://i.postimg.cc/XJR87PR3/17828228261-3cf73de867-b.jpg")

# Create a form to gather all the user inputs.
with st.form(key='fare_form'):
    # Let's get the date and time.
    # The default value is set to the current date and time.
    date = st.date_input("Date of the ride", value=datetime.date.today())
    time = st.time_input("Time of the ride", value=datetime.time(12, 0))

    # Get the pickup and dropoff coordinates using number inputs.
    # The step size is set for more precise input.
    st.markdown("#### Pickup and Dropoff Coordinates")
    col1, col2 = st.columns(2)
    with col1:
        # Changed default values to a valid location in NYC for a working example
        pickup_longitude = st.number_input("Pickup Longitude", value=-73.985655, format="%.6f", step=0.000001)
        pickup_latitude = st.number_input("Pickup Latitude", value=40.757139, format="%.6f", step=0.000001)
    with col2:
        dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.987795, format="%.6f", step=0.000001)
        dropoff_latitude = st.number_input("Dropoff Latitude", value=40.761421, format="%.6f", step=0.000001)

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
