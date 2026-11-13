import urllib.parse
from typing import Optional

def generate_weekly_image_url(topic: str) -> str:
    """Generate a clean, high-resolution dark-mode tech illustration matching @TheAnshumDev style."""
    # Build prompt tailored for X tech graphics (clean, 16:9, dark mode, architectural/technical)
    clean_topic = topic.replace("'", "").replace('"', "")
    prompt = f"minimalist dark mode technical system architecture diagram of {clean_topic}, blueprint schematic, glowing cyan and amber accents, clean vectors, high resolution, 4k, tech twitter visual"
    
    encoded = urllib.parse.quote(prompt)
    # 1200x675 is the official recommended 16:9 dimension for Twitter/X image cards
    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=675&nologo=true&seed=42"
    return image_url
