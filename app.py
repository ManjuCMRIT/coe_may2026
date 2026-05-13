import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Professional Document Scanner")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Generate Clean Scan"):

        # Convert PIL to OpenCV
        img = np.array(image)

        # Resize for better processing
        ratio = img.shape[0] / 500.0
        orig = img.copy()

        resized = cv2.resize(img, (int(img.shape[1] / ratio), 500))

        # Grayscale
        gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)

        # Blur
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Edge detection
        edged = cv2.Canny(gray, 75, 200)

        # Find contours
        contours, _ = cv2.findContours(
            edged.copy(),
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        screenCnt = None

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is not None:

            pts = screenCnt.reshape(4, 2) * ratio

            # Order points
            rect = np.zeros((4, 2), dtype="float32")

            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            (tl, tr, br, bl) = rect

            widthA = np.linalg.norm(br - bl)
            widthB = np.linalg.norm(tr - tl)
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.linalg.norm(tr - br)
            heightB = np.linalg.norm(tl - bl)
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]
            ], dtype="float32")

            # Perspective transform
            M = cv2.getPerspectiveTransform(rect, dst)

            warped = cv2.warpPerspective(
                orig,
                M,
                (maxWidth, maxHeight)
            )

            # Convert to grayscale
            warped_gray = cv2.cvtColor(
                warped,
                cv2.COLOR_RGB2GRAY
            )

            # Adaptive threshold
            scanned = cv2.adaptiveThreshold(
                warped_gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                15,
                15
            )

            # Noise removal
            kernel = np.ones((1, 1), np.uint8)

            scanned = cv2.morphologyEx(
                scanned,
                cv2.MORPH_OPEN,
                kernel
            )

            st.subheader("Clean Scanned Document")
            st.image(scanned, use_container_width=True)

            # Save PDF
            pdf_image = Image.fromarray(scanned)

            pdf_path = "clean_scan.pdf"

            pdf_image.save(pdf_path)

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "Download PDF",
                    pdf_file,
                    file_name="clean_scan.pdf",
                    mime="application/pdf"
                )

        else:
            st.error("Document boundary not detected.")
