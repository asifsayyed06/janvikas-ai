import plotly.express as px
import pandas as pd

def priority_chart(df):
    x = df["priority"].value_counts().rename_axis("Priority").reset_index(name="Requests")
    return px.bar(x, x="Priority", y="Requests", title="Requests by priority")

def category_chart(df):
    x = df["category"].value_counts().rename_axis("Category").reset_index(name="Requests")
    return px.bar(x, x="Category", y="Requests", title="Requests by category")

def status_chart(df):
    x = df["status"].value_counts().rename_axis("Status").reset_index(name="Requests")
    return px.pie(x, names="Status", values="Requests", title="Request status")

def district_chart(df):
    x = df["district"].value_counts().rename_axis("District").reset_index(name="Requests")
    return px.bar(x, x="District", y="Requests", title="Demand by district")

def hotspot_map(df):
    # Demo map: requests are spread around approximate Maharashtra locations.
    coords = {
        "Pune": (18.5204,73.8567),
        "Nashik": (19.9975,73.7898),
        "Ahmednagar": (19.0948,74.7480),
        "Nagpur": (21.1458,79.0882),
        "Mumbai": (19.0760,72.8777),
    }
    d = df.copy()
    d["latitude"] = d.apply(lambda r: coords.get(r["district"], (18.5204,73.8567))[0], axis=1)
    d["longitude"] = d.apply(lambda r: coords.get(r["district"], (18.5204,73.8567))[1], axis=1)
    return px.scatter_mapbox(
        d, lat="latitude", lon="longitude", size="priority_score",
        color="priority", hover_name="title",
        hover_data=["district","ward","category","population_affected"],
        zoom=5, height=550
    ).update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
