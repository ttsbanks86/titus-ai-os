"""Generate a professional AI Tutor icon (.ico) with multiple sizes."""
from PIL import Image, ImageDraw, ImageFont
import math
import os

SIZES = [16, 24, 32, 48, 64, 128, 256]
OUTPUT = os.path.join(os.path.dirname(__file__), "ai_tutor.ico")


def draw_icon(size):
    """Draw the AI Tutor icon at a given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size / 256  # scale factor

    # --- Background: rounded rectangle with gradient feel ---
    # Deep blue-purple base
    bg_color = (30, 25, 75)
    draw.rounded_rectangle(
        [8*s, 8*s, 248*s, 248*s],
        radius=int(40*s),
        fill=bg_color,
    )

    # Subtle inner glow / lighter center
    glow_color = (50, 45, 110)
    draw.rounded_rectangle(
        [20*s, 20*s, 236*s, 236*s],
        radius=int(32*s),
        fill=glow_color,
    )

    # --- Brain / Neural network icon ---
    cx, cy = 128*s, 118*s
    node_r = int(12*s)
    node_color = (100, 200, 255)    # cyan nodes
    edge_color = (80, 160, 230, 180) # blue edges
    accent = (130, 90, 255)          # purple accent nodes

    # Define brain-like node positions (symmetric left/right)
    nodes = [
        # Core (center)
        (cx, cy),
        # Left hemisphere
        (cx - 40*s, cy - 30*s),
        (cx - 65*s, cy - 10*s),
        (cx - 55*s, cy + 20*s),
        (cx - 30*s, cy + 35*s),
        (cx - 70*s, cy + 25*s),
        (cx - 45*s, cy - 50*s),
        # Right hemisphere
        (cx + 40*s, cy - 30*s),
        (cx + 65*s, cy - 10*s),
        (cx + 55*s, cy + 20*s),
        (cx + 30*s, cy + 35*s),
        (cx + 70*s, cy + 25*s),
        (cx + 45*s, cy - 50*s),
        # Top connectors
        (cx, cy - 55*s),
        (cx - 25*s, cy - 65*s),
        (cx + 25*s, cy - 65*s),
    ]

    # Define connections (edges) between nodes
    edges = [
        (0, 1), (0, 7), (0, 13),
        (1, 2), (1, 3), (1, 6), (1, 14),
        (2, 5), (2, 3),
        (3, 4), (3, 5),
        (7, 8), (7, 9), (7, 12), (7, 15),
        (8, 11), (8, 9),
        (9, 10), (9, 11),
        (13, 14), (13, 15),
        (0, 4), (0, 10),
        (6, 14), (12, 15),
    ]

    # Draw edges
    for i, j in edges:
        x1, y1 = nodes[i]
        x2, y2 = nodes[j]
        draw.line([(x1, y1), (x2, y2)], fill=edge_color, width=max(1, int(2*s)))

    # Draw nodes
    for i, (nx, ny) in enumerate(nodes):
        color = accent if i in (0, 6, 12) else node_color
        r = int(node_r * 1.1) if i == 0 else node_r
        draw.ellipse(
            [nx - r, ny - r, nx + r, ny + r],
            fill=color,
        )
        # Inner highlight
        hr = int(r * 0.5)
        highlight = tuple(min(255, c + 60) for c in color[:3])
        draw.ellipse(
            [nx - hr, ny - hr - int(2*s), nx + hr, ny + hr - int(2*s)],
            fill=highlight,
        )

    # --- Graduation cap at top ---
    cap_y = int(28*s)
    cap_cx = cx
    cap_w = int(55*s)
    cap_h = int(14*s)
    tassel_len = int(30*s)

    # Cap base (diamond/rhombus shape)
    cap_points = [
        (cap_cx, cap_y - cap_h),           # top
        (cap_cx + cap_w, cap_y),            # right
        (cap_cx, cap_y + int(6*s)),         # bottom
        (cap_cx - cap_w, cap_y),            # left
    ]
    draw.polygon(cap_points, fill=(60, 50, 120))

    # Cap top band
    draw.rectangle(
        [cap_cx - int(18*s), cap_y - int(8*s),
         cap_cx + int(18*s), cap_y + int(4*s)],
        fill=(70, 60, 140),
    )

    # Tassel line
    tassel_start_x = cap_cx + int(15*s)
    tassel_start_y = cap_y - int(4*s)
    draw.line(
        [(tassel_start_x, tassel_start_y),
         (tassel_start_x + int(8*s), tassel_start_y + tassel_len)],
        fill=(255, 200, 50),
        width=max(1, int(3*s)),
    )
    # Tassel end circle
    draw.ellipse(
        [tassel_start_x + int(4*s), tassel_start_y + tassel_len - int(4*s),
         tassel_start_x + int(12*s), tassel_start_y + tassel_len + int(4*s)],
        fill=(255, 200, 50),
    )

    # --- "AI" text at bottom ---
    text_y = int(195*s)
    try:
        font_size = int(42*s)
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    text = "AI"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = cx - tw // 2
    # Glow behind text
    for offset in range(3, 0, -1):
        alpha = 60 - offset * 15
        glow = (100, 200, 255, alpha)
        draw.text((tx - offset*s, text_y), text, fill=glow, font=font)
        draw.text((tx + offset*s, text_y), text, fill=glow, font=font)
    draw.text((tx, text_y), text, fill=(200, 230, 255), font=font)

    return img


def main():
    images = []
    for size in SIZES:
        img = draw_icon(size)
        # ICO format uses "sizes" param for multi-res
        images.append(img)

    # Save as .ico with all sizes
    images[0].save(
        OUTPUT,
        format="ICO",
        sizes=[(s, s) for s in SIZES],
        append_images=images[1:],
    )
    print(f"Icon saved to: {OUTPUT}")
    print(f"Sizes: {SIZES}")


if __name__ == "__main__":
    main()
