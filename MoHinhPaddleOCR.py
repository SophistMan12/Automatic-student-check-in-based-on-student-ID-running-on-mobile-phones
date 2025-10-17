from paddleocr import PaddleOCR
import re
import os

# === 1️⃣ Đường dẫn ảnh ===
image_path = r"D:\DoAn\imagetest3.jpg"

# === 2️⃣ Khởi tạo PaddleOCR (với hỗ trợ tiếng Việt) ===
ocr = PaddleOCR(lang='vi', use_textline_orientation=True)

# === 3️⃣ OCR ===
results = ocr.predict(image_path)

# === 4️⃣ Gom text lại ===
texts = []
for r in results:
    if isinstance(r, dict) and 'rec_texts' in r:
        texts.extend(r['rec_texts'])
    elif isinstance(r, list):
        for item in r:
            if isinstance(item, dict) and 'rec_texts' in item:
                texts.extend(item['rec_texts'])

clean_texts = [t.strip() for t in texts if t.strip()]
joined = " ".join(clean_texts)

print("\n📜 Kết quả OCR:")
for i, t in enumerate(clean_texts, 1):
    print(f"{i:02d}: {t}")

# === 5️⃣ Sửa lỗi OCR phổ biến ===
fix_map = {
    "Lóp": "Lớp",
    "Khóa hoc": "Khóa học",
    "Tinh": "Tỉnh",
    "Thé": "Thẻ",
    "DAI": "ĐẠI",
    "HOC": "HỌC",
}
for k, v in fix_map.items():
    joined = joined.replace(k, v)

# === 6️⃣ Regex trích xuất thông tin ===
def find(pattern, default=None):
    match = re.search(pattern, joined, re.IGNORECASE)
    return match.group(1).strip() if match else default

# Cải tiến regex nhận diện họ tên (3–4 từ, tiếng Việt có dấu)
name_pattern = r"(?:Tr[aâ]n|Nguy[eê]n|Ph[aà]m|L[eê]|Ho[aà]|V[oõ]|B[uù]i|Ph[aạ]n)\s+[A-ZĐÂÊÔƠƯa-zđâêôơư]+\s+[A-ZĐÂÊÔƠƯa-zđâêôơư]+(?:\s+[A-ZĐÂÊÔƠƯa-zđâêôơư]+)?"

data = {
    "Họ tên": find(name_pattern),
    "Ngày sinh": find(r"NS[:\s]*([\d/]+)"),
    "Lớp": find(r"Lớp[:\s]*([\w-]+)"),
    "Khóa học": find(r"Khóa học[:\s]*([\d\s\-–]+)"),
    "Mã SV": find(r"\b(\d{8})\b"),
}

# === 7️⃣ Xuất kết quả ===
print("\n🧾 Thông tin chính (lọc lại):")
for k, v in data.items():
    print(f"{k}: {v}")

# === 8️⃣ Lưu file txt ===
save_path = os.path.splitext(image_path)[0] + "_result.txt"
with open(save_path, "w", encoding="utf-8") as f:
    f.write("KẾT QUẢ OCR\n")
    for i, t in enumerate(clean_texts, 1):
        f.write(f"{i:02d}: {t}\n")
    f.write("\nTHÔNG TIN CHÍNH:\n")
    for k, v in data.items():
        f.write(f"{k}: {v}\n")

print(f"\n✅ Đã lưu kết quả vào: {save_path}")
