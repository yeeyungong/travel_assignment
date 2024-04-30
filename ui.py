import streamlit as st
import pandas as pd
import requests
import pickle
from PIL import Image
from io import BytesIO

def get_recommendations(location, hashtags_str):
    travel = pd.read_csv("image_dataset.csv")

    # Handle empty hashtags string
    if not hashtags_str:
        return []

    # Split the provided hashtags string into a list
    hashtags = hashtags_str.strip().split()

    # Filter the dataframe based on location (if provided)
    if location:
        filtered_df = travel[travel['location'] == location].copy()  # Make a copy of the filtered DataFrame
        if not filtered_df.empty:
            # Calculate hashtag similarity scores for filtered entries
            filtered_df['hashtag_sim_score'] = filtered_df['hashtag'].apply(
                lambda x: len(set(x.split()) & set(hashtags))
            )
            # Sort entries based on hashtag similarity score
            sorted_df = filtered_df.sort_values(by='hashtag_sim_score', ascending=False)
            # Get top 10 recommendations
            recommendations = sorted_df[['location', 'hashtag', 'image_url']].head(10).to_dict('records')
            return recommendations
    return []

if st.button("Recommend"):
    # Print recommendations if any
    recommendations = get_recommendations(location, hashtags_str)
    if recommendations:
        st.subheader("Recommendations:")
        for recommendation in recommendations:
            st.write(f"- {recommendation['location']}: {recommendation['hashtag']}")
            # Display the image from GitHub repository using the provided URL
            image_url = recommendation['image_url']
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, width=250)
            except Exception as e:
                st.write(f"Error loading image from URL: {image_url}")
                st.write(e)
    else:
        st.write("No recommendations found based on your input.")
