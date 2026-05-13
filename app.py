import streamlit as st
from PIL import Image

st.title("Black and White Image Converter")

# Upload image
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    # Show original image
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Button click
    if st.button("Convert to Black and White"):

        # Convert image to grayscale
        bw_image = image.convert("L")

        # Display converted image
        st.subheader("Black and White Image")
        st.image(bw_image, use_container_width=True)
