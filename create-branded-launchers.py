from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os

base = Path(r"C:\Users\tbank\Desktop\Live Cowork")
desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
icons = base / "app-icons"
icons.mkdir(exist_ok=True)

apps = [
    {
        "name": "EchoKey",
        "letters": "EK",
        "tag": "Local voice dictation",
        "color1": "#3FB950",
        "color2": "#0D1117",
        "target": str(base / "whisper-flow-float.vbs"),
    },
    {
        "name": "SkillVault",
        "letters": "SV",
        "tag": "OpenCode skill store",
        "color1": "#58A6FF",
        "color2": "#161B22",
        "target": str(base / "skill-store" / "index.html"),
    },
    {
        "name": "NoloCast Voice",
        "letters": "NV",
        "tag": "NOLO voice launcher",
        "color1": "#A371F7",
        "color2": "#161B22",
        "target": str(desktop / "NOLO Voice App.vbs"),
    },
    {
        "name": "RelayBoard",
        "letters": "RB",
        "tag": "Telegram board",
        "color1": "#2F81F7",
        "color2": "#0D1117",
        "target": str(desktop / "Telegram Board.vbs"),
    },
    {
        "name": "FlowNode Local",
        "letters": "FN",
        "tag": "Local n8n launcher",
        "color1": "#F97316",
        "color2": "#161B22",
        "target": str(desktop / "Start Local n8n.vbs"),
    },
    {
        "name": "CommandDeck",
        "letters": "CD",
        "tag": "Titus command center",
        "color1": "#D29922",
        "color2": "#0D1117",
        "target": str(desktop / "Titus Command Center.lnk"),
    },
]

try:
    font_big = ImageFont.truetype("arialbd.ttf", 70)
    font_small = ImageFont.truetype("arial.ttf", 14)
except Exception:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

for app in apps:
    size = 256
    img = Image.new("RGBA", (size, size), app["color2"])
    draw = ImageDraw.Draw(img)

    # gradient-ish rings
    draw.rounded_rectangle((18, 18, 238, 238), radius=44, fill=app["color2"], outline=app["color1"], width=6)
    draw.ellipse((62, 42, 216, 196), outline=app["color1"], width=5)
    draw.rectangle((42, 175, 214, 181), fill=app["color1"])

    letters = app["letters"]
    bbox = draw.textbbox((0,0), letters, font=font_big)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((size-tw)/2, 84), letters, font=font_big, fill="#FFFFFF")

    # bottom tag dots
    for i in range(3):
        draw.ellipse((104 + i*22, 205, 114 + i*22, 215), fill=app["color1"])

    ico = icons / f"{app['name'].replace(' ', '-')}.ico"
    img.save(ico, sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
    app["icon"] = str(ico)

# Create shortcuts via COM
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")

dock = desktop / "AI App Dock"
dock.mkdir(exist_ok=True)

for app in apps:
    for folder in [desktop, dock]:
        shortcut_path = folder / f"{app['name']}.lnk"
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = app["target"]
        shortcut.WorkingDirectory = str(Path(app["target"]).parent) if Path(app["target"]).exists() else str(desktop)
        shortcut.Description = app["tag"]
        shortcut.IconLocation = app["icon"]
        shortcut.Save()

print("Created branded icons and shortcuts:")
for app in apps:
    print(f"- {app['name']} -> {app['target']}")
print(f"Icon folder: {icons}")
print(f"Dock folder: {dock}")
