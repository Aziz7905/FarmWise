import os
import json
from django.shortcuts import render

def choropleth_map(request):
    dataset = request.GET.get("dataset", "soter")  # Default GeoJSON file
    variable = request.GET.get("var", "Elev_med")  # Default variable

    geojson_map = {
        "soter": "soter.geojson",
        "params": "params.geojson",
        "units": "units.geojson"
    }

    available_variables = {
        "soter": ["Elev_med", "Slope_med", "Relief_med", "Lithology"],
        "params": ["CFRAG", "BULK", "TAWC", "CECS", "BSAT", "ESP", "PHAQ", "TCEQ", "GYPS", "ELCO", "TOTC", "TOTN", "ALSA"],
        "units": ["DomFAOgrou"]
    }

    filename = geojson_map[dataset]
    path = os.path.join("soil_composition", "static_geo", filename)

    with open(path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    context = {
        "geojson": json.dumps(geojson_data),
        "selected_var": variable,
        "selected_dataset": dataset,
        "available_vars": available_variables[dataset],
        "available_datasets": list(geojson_map.keys())
    }
    return render(request, "soil_composition/soil_lookup.html", context)
