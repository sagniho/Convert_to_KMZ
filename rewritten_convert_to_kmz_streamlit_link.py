
import streamlit as st
import base64
import requests
from math import cos, sin, radians
import simplekml
import os

def geocode_address(address):
    base_url = "https://geocode.maps.co/search"
    full_url = f"{base_url}?q={address}"

    # Make the GET request
    response = requests.get(full_url)
    data = response.json()

    # Check if the response has the expected structure
    if isinstance(data, list) and len(data) > 0 and 'lat' in data[0] and 'lon' in data[0]:
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon
    else:
        st.error(f"Unexpected response from geocoding API: {data}")
        return None, None

# Remaining parts of the script are unchanged...


    base_url = "https://geocode.maps.co/search"
    full_url = f"{base_url}?q={address}"

    # Make the GET request
    response = requests.get(full_url)
    data = response.json()

    # Check if the response has the expected structure
    if 'results' in data and len(data['results']) > 0 and 'geometry' in data['results'][0]:
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
        return lat, lon
    else:
        st.error(f"Unexpected response from geocoding API: {data}")
        return None, None

def create_kmz(lat, lon, filename="RoughAcre", shape="circle"):
    # Create KML document
    kml = simplekml.Kml()
    
    if shape == "circle":
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
    elif shape == "pin":
        kml.newpoint(name=filename, coords=[(lon, lat)])
    
    # Convert KML to KMZ
    kmz_file = f"{filename}.kmz"
    kml.savekmz(kmz_file, format=False)
    
    return kmz_file

def main():
    st.title("Generate KMZ from Address or Coordinates")
    
    # Address input
    address = st.text_input("Enter Address (leave blank if using latitude and longitude):")
    
    # Latitude and Longitude input
    lat = st.text_input("Enter Latitude (leave blank if using address):")
    lon = st.text_input("Enter Longitude (leave blank if using address):")

    # If address is provided, use geocoding to get lat and lon
    if address:
        lat, lon = geocode_address(address)
        st.write(f"Latitude: {lat}, Longitude: {lon}")
    
    # File name input
    filename = st.text_input("Enter a name for the KMZ file (without extension):", "")

    if st.button("Generate KMZ Circle"):
        if lat and lon:
            file_path = create_kmz(lat, lon, filename, shape="circle")
            provide_download_link(file_path)
    elif st.button("Generate KMZ Pin"):
        if lat and lon:
            file_path = create_kmz(lat, lon, filename, shape="pin")
            provide_download_link(file_path)

def provide_download_link(file_path):
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
