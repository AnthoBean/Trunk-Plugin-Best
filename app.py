from PIL import Image, ImageDraw, ImageFont

def render_image(price, trend, forecast, mood, time_updated):
    # Create an 800x480 white image
    img = Image.new("RGB", (800, 480), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_large = ImageFont.truetype("arial.ttf", 48)
    font_medium = ImageFont.truetype("arial.ttf", 32)
    font_small = ImageFont.truetype("arial.ttf", 24)

    # Define positions and sizes
    padding = 20
    section_spacing = 40
    margin_x = 10

    # Background rectangles with darker gray fill
    # Price background
    price_bg_x0 = margin_x
    price_bg_y0 = 50
    price_bg_x1 = 800 - margin_x
    price_bg_y1 = 130
    draw.rounded_rectangle(
        [(price_bg_x0, price_bg_y0), (price_bg_x1, price_bg_y1)],
        radius=15,
        fill=(200, 200, 200)
    )

    # Trend background
    trend_bg_x0 = margin_x
    trend_bg_y0 = price_bg_y1 + section_spacing
    trend_bg_x1 = 800 - margin_x
    trend_bg_y1 = trend_bg_y0 + 60
    draw.rounded_rectangle(
        [(trend_bg_x0, trend_bg_y0), (trend_bg_x1, trend_bg_y1)],
        radius=15,
        fill=(200, 200, 200)
    )

    # Forecast background
    forecast_bg_x0 = margin_x
    forecast_bg_y0 = trend_bg_y1 + section_spacing
    forecast_bg_x1 = 800 - margin_x
    forecast_bg_y1 = forecast_bg_y0 + 60
    draw.rounded_rectangle(
        [(forecast_bg_x0, forecast_bg_y0), (forecast_bg_x1, forecast_bg_y1)],
        radius=15,
        fill=(200, 200, 200)
    )

    # Mood background
    mood_bg_x0 = margin_x
    mood_bg_y0 = forecast_bg_y1 + section_spacing
    mood_bg_x1 = 800 - margin_x
    mood_bg_y1 = mood_bg_y0 + 60
    draw.rounded_rectangle(
        [(mood_bg_x0, mood_bg_y0), (mood_bg_x1, mood_bg_y1)],
        radius=15,
        fill=(200, 200, 200)
    )

    # Center text horizontally within each rectangle
    def draw_centered_text(text, font, y_top, bg_x0, bg_x1):
        text_width, text_height = draw.textsize(text, font=font)
        x = bg_x0 + (bg_x1 - bg_x0 - text_width) // 2
        draw.text((x, y_top + ( ( (bg_x1 - bg_x0) // 10 ) ), text), font=font, fill=(0, 0, 0))
        draw.text((x, y_top + ( ( (bg_x1 - bg_x0) // 10 ) )), text, font=font, fill=(0, 0, 0))
        return

    # Draw price
    price_text = f"{price}¢/kWh"
    price_text_width, price_text_height = draw.textsize(price_text, font=font_large)
    price_x = price_bg_x0 + (price_bg_x1 - price_bg_x0 - price_text_width) // 2
    price_y = price_bg_y0 + ( (price_bg_y1 - price_bg_y0 - price_text_height) // 2 )
    draw.text((price_x, price_y), price_text, font=font_large, fill=(0, 0, 0))

    # Draw trend
    trend_text_width, trend_text_height = draw.textsize(trend, font=font_medium)
    trend_x = trend_bg_x0 + (trend_bg_x1 - trend_bg_x0 - trend_text_width) // 2
    trend_y = trend_bg_y0 + ( (trend_bg_y1 - trend_bg_y0 - trend_text_height) // 2 )
    draw.text((trend_x, trend_y), trend, font=font_medium, fill=(0, 0, 0))

    # Draw forecast
    forecast_text = forecast
    updated_text = f"Updated: {time_updated}"

    forecast_text_width, _ = draw.textsize(forecast_text, font=font_medium)
    updated_text_width, _ = draw.textsize(updated_text, font=font_small)

    forecast_x = forecast_bg_x0 + (forecast_bg_x1 - forecast_bg_x0 - forecast_text_width) // 2
    forecast_y = forecast_bg_y0 + 8  # Slightly down from top

    updated_x = forecast_bg_x0 + (forecast_bg_x1 - forecast_bg_x0 - updated_text_width) // 2
    updated_y = forecast_y + font_medium.size + 4  # More spacing between lines

    draw.text((forecast_x, forecast_y), forecast_text, font=font_medium, fill=(0, 0, 0))
    draw.text((updated_x, updated_y), updated_text, font=font_small, fill=(0, 0, 0))

    # Draw mood
    mood_text_width, mood_text_height = draw.textsize(mood, font=font_medium)
    mood_x = mood_bg_x0 + (mood_bg_x1 - mood_bg_x0 - mood_text_width) // 2
    mood_y = mood_bg_y0 + ( (mood_bg_y1 - mood_bg_y0 - mood_text_height) // 2 )
    draw.text((mood_x, mood_y), mood, font=font_medium, fill=(0, 0, 0))

    # Save image as BMP
    img.save("static/image.bmp")


# Flask app for Render deployment
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    from flask import Flask
    app = Flask(__name__)

    @app.route("/api/display")
    def display():
        from render import render_image
        # Example values, replace with actual logic as needed
        price, trend, forecast, mood, updated = "6.0", "Rising", "Stable", "Good", "5 min ago"
        render_image(price, trend, forecast, mood, updated)
        return {
            "filename": "2025-06-30-plugin-T19:20:57",
            "image_url": "https://trmnl-comed-plugin-sdi1.onrender.com/static/image.bmp",
            "update_firmware": False
        }

    app.run(host="0.0.0.0", port=port, debug=True)