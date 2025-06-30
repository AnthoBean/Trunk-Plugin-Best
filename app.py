from flask import Flask, send_file
from render import render_image
import requests

app = Flask(__name__)

@app.route("/api/display")
def display():
    import datetime
    from flask import jsonify

    try:
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

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-plugin-T%H:%M:%S")

        return jsonify({
            "image_url": "https://trmnl-comed-plugin-sdi1.onrender.com/static/image.bmp",
            "filename": timestamp,
            "update_firmware": False
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "image_url": None,
            "filename": None,
            "update_firmware": False
        }), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)