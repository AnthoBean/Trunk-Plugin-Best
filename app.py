from flask import Flask, send_file
from render import render_image
import requests

app = Flask(__name__)

@app.route("/api/display")
def display():
    url = "https://hourlypricing.comed.com/api?type=5minutefeed"
    response = requests.get(url)
    data = response.json()

    prices = [float(entry["price"]) for entry in data]
    current = prices[-1]
    previous = prices[-2]

    trend = "Trending upward" if current > previous else "Trending downward"
    forecast = "Rising for next 2 hours" if current > previous else "Falling soon"
    mood = (
        "Low price — good time to use electricity" if current < 8 else
        "Moderate price" if current < 15 else
        "High price — avoid usage"
    )

    # Render the BMP
    render_image(f"{current:.2f}", trend, forecast, mood)

    # Construct JSON response
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-plugin-T%H:%M:%S")
    from flask import jsonify
    return jsonify({
        "image_url": "https://trmnl-comed-plugin-sdi1.onrender.com/static/image.bmp",
        "filename": timestamp,
        "update_firmware": False
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)