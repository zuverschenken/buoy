import folium


m = folium.Map(
    location=[58.3258, 10.2969],
    worldCopyJump=True,
    tiles=folium.TileLayer(no_wrap=True),
    zoom_start=8
)


map_script = '<script src="/static/script.js"></script>'
m.get_root().html.add_child(folium.Element(map_script))

m.save("static/interactive_map.html")
print("created interactive map")

