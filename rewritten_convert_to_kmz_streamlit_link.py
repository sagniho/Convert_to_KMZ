
import streamlit as st
import base64
from math import cos, sin, radians
import simplekml
import os

def create_kmz(lat, lon, filename="RoughAcre"):
    # Create KML document
    kml = simplekml.Kml()
    
    # Convert radius from feet to degrees (approximation)
    radius_ft = 10
    radius_deg = radius_ft / 364000  # Approximate conversion for latitude in degrees
    
    # Generate circle points
    num_points = 36  # Adjust the number of points for smoother circles
    angle_increment = 360 / num_points

    polygon = kml.newpolygon(name='Parcel')

    # Create circle vertices
    coords = []
    for i in range(num_points):
        angle = radians(i * angle_increment)
        lat_offset = float(lat) + (radius_deg * cos(angle))
        lon_offset = float(lon) + (radius_deg * sin(angle))
        coords.append((lon_offset, lat_offset))

    polygon.outerboundaryis = coords
    
    # Convert KML to KMZ
    kmz_file = f"{filename}.kmz"
    kml.savekmz(kmz_file, format=False)
    
    return kmz_file

def main():
    st.title("Generate KMZ")
    lat = st.text_input("Enter Latitude:")
    lon = st.text_input("Enter Longitude:")
    filename = st.text_input("Enter a name for the KMZ file (without extension):", "")

    if st.button("Generate KMZ"):
        file_path = create_kmz(lat, lon, filename)
        
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                kmz_data = f.read()
            b64 = base64.b64encode(kmz_data).decode("utf-8")
            href = f'<a href="data:file/kmz;base64,{b64}" download="{file_path}">Click here to download the KMZ file</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Failed to generate KMZ file. Please try again.")

if __name__ == "__main__":
    main()
