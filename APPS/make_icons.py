#!/usr/bin/env python3
"""Generate App Store quality icons for all Titus AI OS apps"""
from PIL import Image, ImageDraw, ImageFont
import os

def rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, r, fill=fill, outline=outline, width=width)

def create_gradient(draw, size, c1, c2):
    for y in range(size[1]):
        r = int(c1[0] + (c2[0]-c1[0]) * y / size[1])
        g = int(c1[1] + (c2[1]-c1[1]) * y / size[1])
        b = int(c1[2] + (c2[2]-c1[2]) * y / size[1])
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))

apps = [
    {
        "name": "EchoKeys",
        "c1": (10, 22, 40), "c2": (26, 42, 74),
        "accent": (138, 180, 248), "light": (168, 200, 255),
        "icon": "mic"
    },
    {
        "name": "NOLA Voice",
        "c1": (11, 15, 26), "c2": (19, 24, 39),
        "accent": (192, 132, 252), "light": (216, 180, 254),
        "icon": "nola"
    },
    {
        "name": "Auto Hub",
        "c1": (10, 15, 10), "c2": (17, 40, 32),
        "accent": (52, 211, 153), "light": (110, 231, 183),
        "icon": "bolt"
    },
    {
        "name": "Job Intel",
        "c1": (10, 26, 15), "c2": (17, 40, 32),
        "accent": (52, 211, 153), "light": (110, 231, 183),
        "icon": "chart"
    },
    {
        "name": "Portfolio",
        "c1": (15, 10, 26), "c2": (26, 17, 40),
        "accent": (96, 165, 250), "light": (147, 197, 253),
        "icon": "globe"
    }
]

output = "C:\\Users\\tbank\\Desktop\\Live Cowork\\APPS"
os.makedirs(output, exist_ok=True)

for app in apps:
    for size in [256, 128, 64]:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Rounded rect background
        margin = max(2, size//64)
        create_gradient(draw, (size, size), app["c1"], app["c2"])
        
        # Glass reflection
        for y in range(size//2):
            alpha = int(15 * (1 - y / (size//2)))
            draw.line([(0, y), (size, y)], fill=(255, 255, 255, alpha))
        
        # Draw accent shapes
        ac = app["accent"]
        lt = app["light"]
        cx, cy = size//2, size//2
        
        if app["icon"] == "mic":
            # Mic body
            mw, mh = size//5, size//3
            draw.rounded_rectangle([cx-mw//2, cy-mh//2, cx+mw//2, cy+mh//2], size//10, fill=lt, outline=None)
            # Mic arc
            draw.chord([cx-mw//2, cy+mh//4-mw//4, cx+mw//2, cy+mh//4+mw//4], 0, 180, fill=lt)
            # Stand
            draw.line([cx, cy+mh//2, cx, cy+mh//2+size//10], fill=lt, width=max(2, size//20))
            draw.line([cx-size//8, cy+mh//2+size//10, cx+size//8, cy+mh//2+size//10], fill=lt, width=max(2, size//20))
        
        elif app["icon"] == "nola":
            # Purple N with glow
            draw.ellipse([cx-size//3, cy-size//3, cx+size//3, cy+size//3], fill=(192, 132, 252, 60), outline=None)
            draw.ellipse([cx-size//4, cy-size//4, cx+size//4, cy+size//4], fill=(192, 132, 252, 40), outline=None)
            # N letter
            try:
                fnt = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", size//2)
                draw.text((cx, cy), "N", fill=lt, font=fnt, anchor="mm")
            except:
                pass
        
        elif app["icon"] == "bolt":
            pts = [(cx, cy-size//3), (cx-size//4, cy), (cx-size//12, cy), (cx, cy+size//3), (cx+size//4, cy), (cx+size//12, cy)]
            draw.polygon(pts, fill=lt)
        
        elif app["icon"] == "chart":
            bar_w = size//8
            gap = size//6
            draw.rectangle([cx-gap-bar_w, cy-size//3, cx-gap, cy+size//3], fill=lt)
            draw.rectangle([cx-bar_w, cy-size//4, cx+bar_w, cy+size//3], fill=lt)
            draw.rectangle([cx+gap, cy-size//5, cx+gap+bar_w, cy+size//3], fill=lt)
            draw.rectangle([cx-gap-bar_w, cy+size//3, cx+gap+bar_w, cy+size//3+size//20], fill=lt)
        
        elif app["icon"] == "globe":
            draw.ellipse([cx-size//3, cy-size//3, cx+size//3, cy+size//3], outline=lt, width=max(2, size//16))
            draw.line([cx-size//3, cy, cx+size//3, cy], fill=lt, width=max(2, size//20))
            
        # Bottom branding bar
        bar_h = size//6
        for y in range(size-bar_h, size):
            ratio = (y - (size-bar_h)) / bar_h
            r = int(ac[0] + (lt[0]-ac[0]) * ratio)
            g = int(ac[1] + (lt[1]-ac[1]) * ratio)
            b = int(ac[2] + (lt[2]-ac[2]) * ratio)
            draw.line([(size//8, y), (size-size//8, y)], fill=(r, g, b))
        
        # App name on bar
        try:
            fnt_sm = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", size//13)
            draw.text((cx, size-bar_h//2), app["name"], fill=app["c1"], font=fnt_sm, anchor="mm")
        except:
            pass
        
        # Save as PNG
        png_path = os.path.join(output, f"{app['name'].replace(' ','')}_{size}.png")
        img.save(png_path)
        
        # Save as ICO (256 version only)
        if size == 256:
            ico_path = os.path.join(output, f"{app['name'].replace(' ','')}.ico")
            img.save(ico_path, format="ICO", sizes=[(256, 256)])
            print(f"OK {app['name']}.ico ({size}x{size})")

print(f"\nAll icons in: {output}")