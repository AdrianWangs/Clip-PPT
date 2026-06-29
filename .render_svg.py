#!/usr/bin/env python3
"""把 CryptoAgent 目录下的 SVG 用 Chrome headless 渲染成 2x PNG。
headless=new 模式下 --window-size 即精确绘制区，输出为 2W x 2H。"""
import re, sys, subprocess, pathlib, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
IMG_DIR = pathlib.Path("/Users/bytedance/Documents/Slidev-PPT/Clip/image/CryptoAgent")
SCALE = 2

def render(svg_path: pathlib.Path):
    svg = svg_path.read_text()
    m = re.search(r'viewBox="([\d.\s-]+)"', svg)
    vb = [float(x) for x in m.group(1).split()]
    W, H = int(round(vb[2])), int(round(vb[3]))
    content = re.sub(r'<\?xml[^>]*\?>', '', svg).strip()
    html = (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            f'*{{margin:0;padding:0}}html,body{{background:#fff}}'
            f'svg{{display:block;width:{W}px;height:{H}px}}</style></head>'
            f'<body>{content}</body></html>')
    with tempfile.TemporaryDirectory() as td:
        hp = pathlib.Path(td) / "p.html"
        hp.write_text(html)
        out = svg_path.with_suffix(".png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                        "--hide-scrollbars", f"--force-device-scale-factor={SCALE}",
                        f"--window-size={W},{H}", f"--screenshot={out}",
                        f"file://{hp}"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dim = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(out)],
                             capture_output=True, text=True).stdout
        pw = re.search(r'pixelWidth: (\d+)', dim)
        ph = re.search(r'pixelHeight: (\d+)', dim)
        print(f"  {svg_path.name} -> {out.name}  viewBox {W}x{H} -> "
              f"{pw.group(1) if pw else '?'}x{ph.group(1) if ph else '?'}")

if __name__ == "__main__":
    targets = sys.argv[1:] or sorted(str(p) for p in IMG_DIR.glob("*.svg"))
    for t in targets:
        render(pathlib.Path(t))
