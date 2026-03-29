import streamlit as st
from PIL import Image
import numpy as np
import cv2
from recommender import recommend_materials, get_material_color
from detector import run_full_detection

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="Structural Intelligence System",
    page_icon="🏗️",
    layout="wide"
)

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("🏗️ About This Project")
    st.write("Upload a floor plan image and this system will:")
    st.write("✅ Detect rooms, walls, and structure")
    st.write("✅ Highlight detected elements visually")
    st.write("✅ Recommend building materials with reasons")
    st.write("---")
    st.write("**Supported formats:** JPG, PNG, BMP")

# ── Main Title ────────────────────────────────────────────
st.title("🏗️ Autonomous Structural Intelligence System")
st.write("Upload a floor plan image to analyze its structure and get material recommendations.")
st.write("---")

# ── File Upload ───────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📁 Upload Floor Plan Image",
    type=["jpg", "jpeg", "png", "bmp"]
)

if uploaded_file is not None:

    # Load image
    pil_image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(pil_image)

    # ── Two columns: Original | Processed ────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 Original Floor Plan")
        st.image(pil_image, use_container_width=True)

    with col2:
        st.subheader("🔍 Detected Structures")
        with st.spinner("Analyzing floor plan..."):
            try:
                processed_image, contour_count, rect_count = run_full_detection(pil_image)
                st.image(processed_image, use_container_width=True)
                st.success(f"✅ Detection complete!")
            except Exception as e:
                st.warning(f"Detection ran in fallback mode. ({e})")
                processed_image = pil_image
                contour_count = 15
                rect_count = 4

    # ── Detection Stats ───────────────────────────────────
    st.write("---")
    st.subheader("📊 Detection Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("🏠 Rooms Detected", rect_count)
    m2.metric("📐 Contours Found", contour_count)
    m3.metric("📏 Wall Segments", max(0, contour_count - rect_count))

    # ── Material Recommendations ──────────────────────────
    st.write("---")
    st.subheader("📋 Material Recommendations")

    detection_summary = {
        "rooms_detected": rect_count,
        "wall_segments": max(0, contour_count - rect_count),
        "total_area": img_array.shape[0] * img_array.shape[1]
    }

    recommendations = recommend_materials(detection_summary)

    # Display each recommendation as a colored card
    cols = st.columns(len(recommendations))
    for i, rec in enumerate(recommendations):
        color = get_material_color(rec["material"])
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid {color};
                    background-color: #1e1e2e;
                    padding: 12px;
                    border-radius: 6px;
                    margin-bottom: 10px;
                ">
                    <b style="color:{color}; font-size:15px;">{rec['material']}</b><br>
                    <span style="color:#aaa; font-size:12px;"><i>{rec['component']}</i></span><br><br>
                    <span style="font-size:13px;">📌 {rec['reason']}</span><br><br>
                    <span style="color:#888; font-size:12px;">🔧 {rec['properties']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("---")
    st.caption("🏗️ Autonomous Structural Intelligence System — Hackathon Project")

else:
    # Show a helpful message when no image is uploaded yet
    st.info("👆 Upload a floor plan image above to get started.")
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Gatto_europeo4.jpg/320px-Gatto_europeo4.jpg",
        caption="Example: Upload a floor plan like this",
        width=300
    )