from PIL import Image, ImageDraw, ImageFont
import datetime
import os
from textwrap import wrap

def render_image(price, trend, forecast, mood):
    W, H = 800, 480
    image = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    box_color = (240, 240, 240)
    border_color = (200, 200, 200)
    mood_colors = {
        "Low price — good time to use electricity": (200, 255, 200),
        "Moderate price": (255, 255, 200),
        "High price — avoid usage": (255, 200, 200)
    }

    font_path = "segoeuithis.ttf"
    font_large = ImageFont.truetype(font_path, 40)
    font_medium = ImageFont.truetype(font_path, 28)
    font_small = ImageFont.truetype(font_path, 20)

    boxes = [
        {"title": "current price", "content": f"{price}¢/kWh"},
        {"title": "mood", "content": mood},
        {"title": "trend", "content": trend},
        {"title": "forecast", "content": forecast},
    ]

    now = datetime.datetime.now()
    updated_time = "updated just now"

    box_width = 370
    box_height = 200
    spacing = 30

    for i, box in enumerate(boxes):
        x = spacing + (i % 2) * (box_width + spacing)
        y = spacing + (i // 2) * (box_height + spacing)
        box_outline = mood_colors.get(box["content"], box_color) if box["title"] == "mood" else box_color

        draw.rounded_rectangle(
            [x, y, x + box_width, y + box_height],
            radius=20,
            fill=box_outline,
            outline=border_color,
            width=2
        )

        draw.text((x + 20, y + 20), box["title"], font=font_small, fill="black")
        text_box_width = box_width - 40
        wrapped_lines = wrap(box["content"], width=22)
        line_height = font_medium.getbbox("A")[3] - font_medium.getbbox("A")[1] + 6
        for j, line in enumerate(wrapped_lines):
            draw.text((x + 20, y + 80 + j * line_height), line, font=font_medium, fill="black")

        # Draw updated_time inside the forecast box
        if box["title"] == "forecast":
            update_w, update_h = font_small.getbbox(updated_time)[2:]
            update_x = x + box_width - update_w - 20
            update_y = y + box_height - update_h - 20
            draw.text((update_x, update_y), updated_time, font=font_small, fill="gray")


    image.save("static/image.bmp")
    # Notify TRMNL via webhook
    import requests
    try:
        requests.get("https://usetrmnl.com/api/custom_plugins/498803d1-bff0-4f07-8622-350eafe5588d")
    except Exception as e:
        print("Failed to notify TRMNL:", e)

import os
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
