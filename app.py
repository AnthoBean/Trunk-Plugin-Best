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

        latest = data[0]
        previous = data[1]
        current = float(latest["price"])

        trend = "Trending upward" if current > float(previous["price"]) else "Trending downward"
        forecast = "Rising for next 2 hours" if current > float(previous["price"]) else "Falling soon"
        mood = (
            "Low price — good time to use electricity" if current < 8 else
            "Moderate price" if current < 15 else
            "High price — avoid usage"
        )

        from datetime import datetime, timezone

        millis = int(latest["millisUTC"])
        updated_time = datetime.fromtimestamp(millis / 1000, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        minutes_ago = int((now - updated_time).total_seconds() / 60)
        updated_str = f"{minutes_ago} min ago"

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