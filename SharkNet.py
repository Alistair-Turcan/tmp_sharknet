import streamlit as st
st.title("SharkNet: Automatic Breast Cancer Classification from Thermography")
st.set_page_config(
    page_title="SharkNet"
)

st.write("hello")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
st.image(
    uploaded_file, caption=f"Original image", use_column_width=True,
)

#process the image thru the stuff
salient_image = uploaded_file

probability = 0
st.write("Probability of tumor presence: " + str(probability) + "%.")
st.write("Processed Image")
st.write("Red dots indicate points of interest.")
st.image(
    salient_image, caption=f"Processed image", use_column_width=True,
)
