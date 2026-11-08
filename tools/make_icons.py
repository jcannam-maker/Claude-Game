"""Draw the DCF calculator app icon at several sizes (PNG + macOS .icns)."""
import io, struct, sys
from pathlib import Path
from PIL import Image, ImageDraw

def draw(size: int) -> Image.Image:
    S = 1024
    im = Image.new("RGB", (S, S), "#1f6feb")
    d = ImageDraw.Draw(im)
    # subtle vertical gradient
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=(int(31 + 10 * t), int(111 - 40 * t), int(235 - 60 * t)))
    # rising bars
    base, w, gap, x0 = 800, 130, 50, 190
    for i, h in enumerate([200, 290, 390, 500]):
        x = x0 + i * (w + gap)
        d.rounded_rectangle([x, base - h, x + w, base], radius=22, fill=(255, 255, 255, 255))
    # trend line
    pts = [(x0 + w / 2 + i * (w + gap), base - h - 70) for i, h in enumerate([200, 290, 390, 500])]
    d.line(pts, fill="#ffd54a", width=34, joint="curve")
    for p in pts:
        d.ellipse([p[0] - 30, p[1] - 30, p[0] + 30, p[1] + 30], fill="#ffd54a")
    d.line([(150, base + 40), (S - 150, base + 40)], fill=(255, 255, 255), width=18)
    return im.resize((size, size), Image.LANCZOS)

def rounded(im: Image.Image) -> Image.Image:
    """macOS icons carry their own rounded-rect shape with transparent margin."""
    S = im.size[0]
    pad = int(S * 0.1)
    inner = im.resize((S - 2 * pad, S - 2 * pad), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", inner.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, *inner.size], radius=int(inner.size[0] * 0.225), fill=255)
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    out.paste(inner, (pad, pad), mask)
    return out

def icns(path: Path):
    entries = b""
    for code, size in [(b"ic07", 128), (b"ic08", 256), (b"ic09", 512), (b"ic10", 1024)]:
        buf = io.BytesIO(); rounded(draw(size)).save(buf, "PNG")
        data = buf.getvalue()
        entries += code + struct.pack(">I", len(data) + 8) + data
    path.write_bytes(b"icns" + struct.pack(">I", len(entries) + 8) + entries)

if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for s in (180, 192, 512):
        draw(s).save(out / f"icon-{s}.png", optimize=True)
    if len(sys.argv) > 2:
        icns(Path(sys.argv[2]))
