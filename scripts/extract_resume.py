import pymupdf

doc = pymupdf.open(r"C:\Users\raghu\Documents\certificates\Sumit_aiml resume .pdf")
out = []
for i, p in enumerate(doc):
    t = p.get_text("text")
    out.append(f"===== PAGE {i+1} =====\n" + t)
text = "\n".join(out)
with open("_resume_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("pages:", len(doc), "| chars:", len(text))
