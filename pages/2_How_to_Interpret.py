import streamlit as st
st.set_page_config(page_title="How to Interpret")
st.title("How to Interpret")

st.write("After uploading your thermograph, 2 results will be shown to you.")
st.write("One, is the patient's chance of having a tumor given the thermograph.")
st.write("The second result is called a saliency map. It will indicate what areas of the image were deemed most important in determining the above probability. Areas colored brighter are deemed more important.")
st.write("Both caregivers and patients can look at the saliency map to evaluate their trust in the model's prediction. It can also aid in the self examination of the patient by showing the area where a tumor has been identified.")
st.write("This is not meant as an alternative to more robust techniques like mammography. It is meant to advise those who can't afford get routine mammographies in if they need further testing.")
