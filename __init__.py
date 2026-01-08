from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
@app.route("/commits-data/")
def commits_data():
    
    api_url = "https://api.github.com/repos/elwintsolefack/5MCSI_Metriques/commits?per_page=100"

    # GitHub demande souvent un User-Agent
    req = Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    response = urlopen(req)
    raw_content = response.read()
    commits_json = json.loads(raw_content.decode("utf-8"))

    counts = defaultdict(int)

    for c in commits_json:
        date_string = c.get("commit", {}).get("author", {}).get("date")
        if not date_string:
            continue

        dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        minute_key = dt.strftime("%Y-%m-%d %H:%M")  # regroupement par minute
        counts[minute_key] += 1

    results = [{"minute": k, "count": counts[k]} for k in sorted(counts.keys())]
    return jsonify(results=results)
@app.route("/commits/")
def commits_page():
    return render_template("commits.html")

if __name__ == "__main__":
  app.run(debug=True)
