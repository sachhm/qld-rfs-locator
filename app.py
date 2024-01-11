from flask import Flask
from flask import render_template, url_for, request
import qld_rfs

app = Flask(__name__)

@app.route('/')
def home():
    """Handle home page"""
    return render_template("home.html")

@app.route('/locate', methods=['POST'])
def locate():
    """Locate nearest QLD RFS station"""
    street_no = int(request.form['street_no'])
    street = request.form['street']
    locality = request.form['locality']
    user_address = f"{street_no} {street}, {locality}"

    # Find closest 
    geocoding_request_url = qld_rfs.make_api_request(street_no, street, locality)
    lat, long = qld_rfs.extract_lat_long(geocoding_request_url)
    closest_rfs = qld_rfs.find_closest_location(lat, long, qld_rfs.QLD_RFS)
    closest_rfs_formatted = f"{closest_rfs["STATION"]}, {closest_rfs["ADDRESS"]}, {closest_rfs["LOCALITY"]}"


    return render_template("home.html", user_address=user_address, lat=lat, long=long,closest_rfs=closest_rfs_formatted)


@app.route('/about')
def about():
    """Handle about page"""
    return render_template("about.html")

if __name__ == '__main__':
    app.run()
