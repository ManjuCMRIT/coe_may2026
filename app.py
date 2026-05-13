import streamlit as st
from PIL import Image, ImageOps

st.title("Image to PDF Converter")

uploaded_file = st.file_uploader(
    "Upload Page Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to PDF Style"):

        # Convert to grayscale
        gray = ImageOps.grayscale(image)

        # Increase contrast / threshold
        bw = gray.point(lambda x: 0 if x < 150 else 255, '1')

        st.subheader("Processed Page")
        st.image(bw, use_container_width=True)

        # Save as PDF
        pdf_path = "output.pdf"
        bw.save(pdf_path)

        # Download button
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="converted_page.pdf",
                mime="application/pdf"
            )
