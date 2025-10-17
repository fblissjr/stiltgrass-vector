#!/usr/bin/env python3
"""
Create interactive map with all treasure hunt data layers
"""

import json
import pandas as pd
import folium
from folium import plugins

def create_treasure_map():
    """Create comprehensive interactive map"""
    print("Creating treasure hunt interactive map...")

    # Center on Day 8 search area
    day8_center = [35.705, -82.83]
    day8_radius_miles = 87 / 2  # diameter to radius

    # Create base map
    m = folium.Map(
        location=day8_center,
        zoom_start=10,
        tiles='OpenStreetMap'
    )

    # Add tile layers
    folium.TileLayer('OpenTopoMap', name='Topographic').add_to(m)
    folium.TileLayer('CartoDB positron', name='Light').add_to(m)

    # Define search circles for Days 1-8
    search_circles = [
        {'day': 1, 'center': [37.5, -82.0], 'diameter': 420, 'color': 'gray'},
        {'day': 2, 'center': [37.0, -82.0], 'diameter': 340, 'color': 'lightgray'},
        {'day': 3, 'center': [36.7, -82.1], 'diameter': 270, 'color': 'lightblue'},
        {'day': 4, 'center': [36.3, -82.4], 'diameter': 210, 'color': 'blue'},
        {'day': 5, 'center': [36.15, -82.67], 'diameter': 160, 'color': 'purple'},
        {'day': 6, 'center': [35.925, -82.85], 'diameter': 120, 'color': 'orange'},
        {'day': 7, 'center': [35.79, -82.8], 'diameter': 100, 'color': 'yellow'},
        {'day': 8, 'center': [35.705, -82.83], 'diameter': 87, 'color': 'red'},
    ]

    # Add search circles
    for circle in search_circles:
        folium.Circle(
            location=circle['center'],
            radius=circle['diameter'] / 2 * 1609.34,  # miles to meters
            color=circle['color'],
            fill=False,
            weight=2,
            popup=f"Day {circle['day']}: {circle['diameter']} mi diameter",
            tooltip=f"Day {circle['day']}",
            opacity=0.5 if circle['day'] < 8 else 0.8
        ).add_to(m)

    # Load top candidates
    try:
        top_candidates = pd.read_csv('data/final_top_20.csv')
        print(f"Loaded {len(top_candidates)} top candidates")
    except FileNotFoundError:
        print("Warning: final_top_20.csv not found, skipping candidates")
        top_candidates = None

    # Load GeoJSON trail data to get coordinates
    with open('data/trails.geojson') as f:
        trail_geojson = json.load(f)

    # Create a mapping of OSM IDs to trail features
    trail_map = {}
    for feature in trail_geojson['features']:
        osm_id = feature['properties'].get('id', '')
        trail_map[osm_id] = feature

    # Add top 20 candidates as markers
    if top_candidates is not None:
        for i, row in top_candidates.head(20).iterrows():
            osm_id = row['osm_id']
            if osm_id in trail_map:
                trail_feature = trail_map[osm_id]
                coords = trail_feature['geometry']['coordinates']

                # Get midpoint of trail for marker
                if len(coords) > 0:
                    if len(coords) == 1:
                        mid_lat, mid_lon = coords[0][1], coords[0][0]
                    else:
                        mid_idx = len(coords) // 2
                        mid_lon, mid_lat = coords[mid_idx]

                    # Color code by rank
                    if i < 3:
                        icon_color = 'red'
                        icon_icon = 'star'
                    elif i < 10:
                        icon_color = 'orange'
                        icon_icon = 'flag'
                    else:
                        icon_color = 'blue'
                        icon_icon = 'info-sign'

                    # Create popup with details
                    popup_html = f"""
                    <div style="font-family: Arial; width: 250px;">
                        <h4>#{i+1}: {row['trail_name']}</h4>
                        <b>Score:</b> {row['total_score']:.0f}/130<br>
                        <b>Length:</b> {row['distance_miles']:.2f} miles<br>
                        <b>Surface:</b> {row['surface']}<br>
                        <b>Difficulty:</b> {row['difficulty']}<br>
                        <b>Type:</b> {row['highway_type']}<br>
                        <b>County:</b> {row['county']}<br>
                    </div>
                    """

                    folium.Marker(
                        location=[mid_lat, mid_lon],
                        popup=folium.Popup(popup_html, max_width=300),
                        tooltip=f"#{i+1}: {row['trail_name']}",
                        icon=folium.Icon(color=icon_color, icon=icon_icon)
                    ).add_to(m)

                    # Add the trail polyline
                    trail_coords = [[coord[1], coord[0]] for coord in coords]
                    folium.PolyLine(
                        trail_coords,
                        color=icon_color,
                        weight=4,
                        opacity=0.7,
                        popup=f"#{i+1}: {row['trail_name']}"
                    ).add_to(m)

    # Add legend
    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 200px; height: auto;
                background-color: white; z-index:9999; font-size:14px;
                border:2px solid grey; border-radius: 5px; padding: 10px">
    <h4 style="margin-top:0;">Legend</h4>
    <p><span style="color:red;">&#9733;</span> Top 3 Candidates</p>
    <p><span style="color:orange;">&#9873;</span> Top 4-10 Candidates</p>
    <p><span style="color:blue;">&#9432;</span> Top 11-20 Candidates</p>
    <p><span style="color:red;">&#9711;</span> Day 8 Search Area</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add layer control
    folium.LayerControl().add_to(m)

    # Add fullscreen button
    plugins.Fullscreen().add_to(m)

    # Save map
    output_file = 'treasure_map.html'
    m.save(output_file)
    print(f"Map saved to: {output_file}")

    return output_file

if __name__ == '__main__':
    create_treasure_map()
