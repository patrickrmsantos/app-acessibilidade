from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def buscar_locais_acessiveis(lat, lon):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["wheelchair"="yes"](around:1000,{lat},{lon});
      way["wheelchair"="yes"](around:1000,{lat},{lon});
      node["toilets:wheelchair"="yes"](around:1000,{lat},{lon});
      way["toilets:wheelchair"="yes"](around:1000,{lat},{lon});
      node["ramp"="yes"](around:1000,{lat},{lon});
      way["ramp"="yes"](around:1000,{lat},{lon});
    );
    out center;
    """
    response = requests.post(overpass_url, data={"data": query})
    data = response.json()
    locais = []
    for elemento in data["elements"]:
        nome = elemento.get("tags", {}).get("name", "Local acessível")
        lat = elemento.get("lat") or elemento.get("center", {}).get("lat")
        lon = elemento.get("lon") or elemento.get("center", {}).get("lon")
        locais.append({"nome": nome, "lat": lat, "lon": lon})
    return locais

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.get_json()
    lat = dados["lat"]
    lon = dados["lon"]
    locais = buscar_locais_acessiveis(lat, lon)
    return jsonify(locais)

if __name__ == "__main__":
    app.run(debug=True)
