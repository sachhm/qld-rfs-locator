from flask import Flask
from flask import render_template, url_for, request
import qld_rfs

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/locate', methods=['POST'])
def locate():
    street_no = float(request.form['street_no'])
    street = request.form['street']
    locality = request.form['locality']

    # Call your geocoding and fire station functions
    geocoding_request_url = qld_rfs.make_api_request(street_no, street, locality)
    lat, long = qld_rfs.extract_lat_long(geocoding_request_url)
    closest_rfs_lat = qld_rfs.find_closest_value_pandas(lat, qld_rfs.QLD_RFS["LAT_GDA20"])
    closest_rfs_long = qld_rfs.find_closest_value_pandas(long, qld_rfs.QLD_RFS["LONG_GDA20"])

    closest_rfs = qld_rfs.QLD_RFS[qld_rfs.QLD_RFS["LAT_GDA20"] == closest_rfs_lat]
    closest_rfs = qld_rfs.QLD_RFS[qld_rfs.QLD_RFS["LONG_GDA20"] == closest_rfs_long]

    return render_template("home.html", closest_rfs=closest_rfs)



@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run()
