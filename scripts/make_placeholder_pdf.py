import os

stream = (
    "BT /F1 24 Tf 72 720 Td (Sumit Raghuwanshi - Resume) Tj ET\n"
    "BT /F1 12 Tf 72 680 Td (Replace this placeholder file with your real resume PDF.) Tj ET\n"
    "BT /F1 12 Tf 72 660 Td (Just save it as: assets/resume.pdf) Tj ET\n"
)

objs = [
    "<</Type/Catalog/Pages 2 0 R>>",
    "<</Type/Pages/Kids[3 0 R]/Count 1>>",
    "<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>",
    f"<</Length {len(stream)}>>stream\n{stream}endstream",
    "<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>",
]

out = b"%PDF-1.4\n"
offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(out))
    out += (f"{i} 0 obj{o}endobj\n").encode("latin-1")

xref_pos = len(out)
out += f"xref\n0 {len(objs)+1}\n".encode()
out += b"0000000000 65535 f \n"
for off in offsets:
    out += f"{off:010d} 00000 n \n".encode()
out += f"trailer<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{xref_pos}\n%%EOF".encode()

os.makedirs("assets", exist_ok=True)
with open("assets/resume.pdf", "wb") as f:
    f.write(out)
print("wrote assets/resume.pdf", len(out), "bytes")
