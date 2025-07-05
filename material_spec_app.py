# Material Specification Web App - Full Streamlit Code with Supabase Integration

import streamlit as st
import pandas as pd
import os
from datetime import date
from PIL import Image
from fpdf import FPDF
import plotly.express as px
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://elanyyvekehahxslujkj.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsYW55eXZla2VoYWh4c2x1amtqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE3MzUwOTQsImV4cCI6MjA2NzMxMTA5NH0.8GxojDJIdniKcfR00rfB5vvMCCMq7Qrznms2omrv5VE"  # Replace with your Supabase anon/public key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Paths
IMAGE_DIR = 'uploaded_images'
LOGO_PATH = 'Artboard 2.png'

# Ensure image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load logo
st.set_page_config(page_title="Material Spec Manager - By Aadil Sukry", layout="wide")
logo = Image.open(LOGO_PATH)
st.image(logo, width=150)

st.title("📋 Material Specification Manager")

# PDF export function
def export_to_pdf(data, output_path, logo_path=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for index, row in data.iterrows():
        pdf.add_page()
        if logo_path and os.path.exists(logo_path):
            pdf.image(logo_path, x=10, y=8, w=40)
            pdf.set_y(30)
        pdf.set_font("Arial", size=12)
        for key, value in row.items():
            if key == 'Image Path' and isinstance(value, str) and os.path.exists(value):
                pdf.ln(5)
                pdf.image(value, w=80)
                pdf.ln(5)
            else:
                pdf.multi_cell(0, 8, f"{key}: {value}", 0)
                pdf.ln(1)
    pdf.output(output_path)
    return output_path

# Load data from Supabase
@st.cache_data(ttl=600)
def load_data():
    response = supabase.table("materials").select("*").execute()
    return pd.DataFrame(response.data)

def save_data(entry):
    supabase.table("materials").insert(entry).execute()

# Tabs
page = st.sidebar.selectbox("Navigate", ["Add Material", "View Report", "Analytics Dashboard", "Project Dashboard"])

data = load_data()

if page == "Add Material":
    st.subheader("➕ Add New Material Specification")
    with st.form("material_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input("Project Name")
            location = st.text_input("Location")
            id_package = st.text_input("ID Package Ref")
            prepared_by = st.text_input("Prepared By")
            mat_name = st.text_input("Material/Item Name")
            mat_category = st.selectbox("Material Category", ["Furniture", "Finishes", "Joinery", "Loose FF&E", "Wall Treatment", "Flooring", "Ceiling", "Architectural Detail"])
            area = st.text_input("Area of Application")
            ref_code = st.text_input("Reference Code")
            mat_type = st.text_input("Type")
            brand = st.text_input("Brand / Manufacturer")
            model = st.text_input("Model / Collection Name")
            color = st.text_input("Finish / Color / Pattern")
        with col2:
            dimensions = st.text_input("Dimensions")
            thickness = st.text_input("Thickness / Weight / Density")
            texture = st.text_input("Texture / Surface Treatment")
            edge_detail = st.text_input("Edge / Joint Detail")
            substrate = st.text_input("Substrate")
            fire_rating = st.text_input("Fire Rating / Classification")
            voc = st.text_input("VOC / Sustainability Certs")
            durability = st.text_input("Durability / Abrasion Rating")
            warranty = st.text_input("Warranty / Lifespan")
            fixing = st.text_input("Fixing Method")
            maintenance = st.text_input("Maintenance Guidelines")
            supplier = st.text_input("Supplier Name / Contact")
            origin = st.text_input("Country of Origin")
            lead_time = st.text_input("Lead Time")
        image = st.file_uploader("Upload Material Image", type=["png", "jpg", "jpeg"])
        submit = st.form_submit_button("Submit")
        if submit:
            img_path = ""
            if image:
                img_path = os.path.join(IMAGE_DIR, image.name)
                with open(img_path, "wb") as f:
                    f.write(image.read())
            entry = {
                "Project Name": project_name, "Location": location, "ID Package Ref": id_package, "Prepared By": prepared_by, "Date": str(date.today()),
                "Material/Item Name": mat_name, "Material Category": mat_category, "Area of Application": area, "Reference Code": ref_code,
                "Type": mat_type, "Brand / Manufacturer": brand, "Model / Collection Name": model, "Finish / Color / Pattern": color,
                "Dimensions": dimensions, "Thickness / Weight / Density": thickness, "Texture / Surface Treatment": texture,
                "Edge / Joint Detail": edge_detail, "Primary Material(s)": "", "Substrate": substrate, "Fire Rating / Classification": fire_rating,
                "VOC Compliance / Sustainability Certs": voc, "Durability / Abrasion Rating": durability, "Acoustic / Thermal Performance": "",
                "Water / Moisture Resistance": "", "Warranty / Lifespan": warranty, "Substrate Requirement": "", "Fixing Method": fixing,
                "Installation Notes": "", "Maintenance Guidelines": maintenance, "Supplier Name / Contact": supplier,
                "Country of Origin": origin, "Lead Time": lead_time, "MOQ": "", "Unit of Measure": "", "Unit Cost": "", "Sample Status": "",
                "Image Path": img_path
            }
            save_data(entry)
            st.success("✅ Material specification saved to Supabase!")

# Remaining pages (View Report, Analytics, Project Dashboard) remain unchanged but should work off 'data' variable
