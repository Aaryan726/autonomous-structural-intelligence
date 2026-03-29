import cv2
import numpy as np
from PIL import Image


def preprocess_image(image):
    """Convert to grayscale, blur, and detect edges."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 30, 100)
    return edges


def find_contours(edge_image):
    """Find and filter contours by minimum area."""
    contours, _ = cv2.findContours(
        edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    valid = [c for c in contours if cv2.contourArea(c) > 200]
    return valid


def detect_rectangles(contours, original_image):
    """Detect rectangles and draw them on the image."""
    annotated = original_image.copy()
    rect_count = 0

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            rect_count += 1
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h

            # Color code by size
            if area > 20000:
                color = (0, 0, 255)    # Red = large zone
                label = "Zone"
            elif area > 5000:
                color = (0, 255, 0)    # Green = room
                label = "Room"
            else:
                color = (255, 165, 0)  # Orange = small space
                label = "Space"

            cv2.drawContours(annotated, [approx], -1, color, 2)
            cv2.putText(
                annotated, label, (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
            )

    return annotated, rect_count


def run_full_detection(pil_image):
    """
    Main function called by app.py.
    Takes a PIL image, returns processed PIL image + counts.
    """
    # Convert PIL to OpenCV format
    img_array = np.array(pil_image)
    cv_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # Run detection pipeline
    edges = preprocess_image(cv_image)
    contours = find_contours(edges)
    annotated, rect_count = detect_rectangles(contours, cv_image)

    # Convert back to RGB for Streamlit
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    result_pil = Image.fromarray(annotated_rgb)

    return result_pil, len(contours), rect_count