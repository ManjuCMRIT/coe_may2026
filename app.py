import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Clean Document Scanner")

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Read image
    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Generate Clean Scan"):

        # Convert PIL image to OpenCV format
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Remove noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive threshold for clean document
        scanned = cv2.adaptiveThreshold(
            blur,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        st.subheader("Clean Scanned Output")
        st.image(scanned, use_container_width=True)

        # Save as PDF
        scanned_pil = Image.fromarray(scanned)

        pdf_path = "clean_document.pdf"

        scanned_pil.save(pdf_path)

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="clean_document.pdf",
                mime="application/pdf"
            )
