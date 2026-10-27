"""Turn the user's background-removed portrait into the site's theme.

- trims transparent padding
- recolours the bright green tee to the site's crimson (keeps shading + white print)
- upscales with LANCZOS + light unsharp mask so it stays crisp in the hero
"""
from PIL import Image, ImageFilter

SRC = r"C:\Users\raghu\Pictures\my_img_prof-removebg-preview.png"
OUT = "assets/photo-cutout.png"

im = Image.open(SRC).convert("RGBA")
im = im.crop(im.split()[3].getbbox())

px = im.load()
w, h = im.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        # green-dominant pixels = the tee (skin / black jacket / white print untouched)
        mx, mn = max(r, g, b), min(r, g, b)
        sat = 0 if mx == 0 else (mx - mn) / mx
        if mx == g and sat > 0.22 and g > 40:
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            if lum < 0.09:      # dark folds stay dark
                nr, ng, nb = r, g, b
            else:
                # map luminance onto the crimson ramp
                t = min(1.0, max(0.0, (lum - 0.09) / 0.88))
                nr = int(22 + (231 - 22) * t ** 1.2)
                ng = int(5 + (56 - 5) * t ** 1.35)
                nb = int(10 + (64 - 10) * t ** 1.35)
            px[x, y] = (nr, ng, nb, a)

big = im.resize((int(w * 2.6), int(h * 2.6)), Image.LANCZOS)
r, g, b, a = big.split()
rgb = Image.merge("RGB", (r, g, b)).filter(
    ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=2)
)
out = Image.merge("RGBA", (*rgb.split(), a))
out.save(OUT)
print("saved", OUT, out.size)

bg = Image.new("RGB", out.size, (10, 6, 7))
bg.paste(out, (0, 0), out)
bg.resize((int(out.width * 0.5), int(out.height * 0.5))).save(
    "screenshots/_newphoto_s.jpg", quality=88
)
