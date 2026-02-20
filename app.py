import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Civil Engineering Insight Studio",
    page_icon="🏗️",
    layout="centered"
)

st.title("🏗️ Civil Engineering Insight Studio")
st.caption("AI-assisted structural understanding using image and engineering context")

# -------------------------------------------------
# User Input Prompt (PROJECT FLOW ✔)
# -------------------------------------------------
user_prompt = st.text_area(
    "📝 Input Prompt",
    placeholder="Example: Analyze the structural damage, identify possible failure causes, and give safety recommendations.",
    height=120
)

# -------------------------------------------------
# Load BLIP Model
# -------------------------------------------------
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    return processor, model

processor, model = load_model()

# -------------------------------------------------
# Engineering Report Generator (LONG FORM)
# -------------------------------------------------
def generate_engineering_report(caption, prompt):
    report = f"""
### 1. Overview of the Structure

Based on the uploaded image, the structure can be described as follows:
{caption}. The visible condition of the structure suggests notable concerns from a civil engineering perspective.

### 2. Structural Condition Assessment

From visual inspection, several indicators point toward potential structural distress. These may include damage to load-bearing components, degradation of reinforced concrete elements, and signs of material failure. The observed condition implies that the structure may have experienced excessive loading, poor maintenance, environmental exposure, or extreme external events.

### 3. Possible Causes of Damage

Potential contributing factors include:
- Aging and long-term material deterioration
- Inadequate structural design or construction defects
- Environmental effects such as moisture ingress or corrosion
- Overloading beyond design limits
- Seismic or impact-related forces

### 4. Engineering Interpretation (User Context)

User-requested focus:
{prompt if prompt else "General structural safety and condition evaluation."}

Considering the above context, the structure exhibits conditions that require professional evaluation. Visual indicators alone are insufficient for final judgment, but they strongly suggest the need for immediate technical attention.

### 5. Safety Evaluation

The current visible state of the structure may pose safety risks to occupants and nearby infrastructure. Falling debris, progressive collapse, or sudden failure are possible if corrective measures are not taken.

### 6. Engineering Recommendations

- Conduct a detailed on-site structural inspection by a licensed civil or structural engineer.
- Perform non-destructive tests (Rebound Hammer, Ultrasonic Pulse Velocity).
- Assess reinforcement corrosion and concrete integrity.
- Restrict access to the structure until safety is verified.
- Plan for strengthening, retrofitting, or demolition based on assessment results.

### 7. Conclusion

This AI-assisted analysis provides an initial understanding of the structure using image-based interpretation combined with engineering reasoning. Final decisions must be based on detailed calculations, field testing, and professional judgment.
"""

    return report.strip()

# -------------------------------------------------
# Image Upload
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "🖼️ Choose an image (JPG / JPEG / PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("🚀 Describe Structure"):
        with st.spinner("Generating detailed engineering report..."):

            inputs = processor(image, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(**inputs)

            caption = processor.decode(
                output[0], skip_special_tokens=True
            )

            report = generate_engineering_report(caption, user_prompt)

        st.success("Analysis Complete")

        st.subheader("🧠 AI-Generated Engineering Report")
        st.markdown(report)

        st.warning(
            "⚠️ This report is AI-assisted and must be validated by a qualified civil engineer before implementation."
        )
