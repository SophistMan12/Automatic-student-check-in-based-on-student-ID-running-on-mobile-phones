import os
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
import barcode
from barcode.writer import ImageWriter

# ==== Config ====
MM_TO_INCH = 0.0393701
DPI = 300
CARD_WIDTH_MM = 81
CARD_HEIGHT_MM = 51

W = int(CARD_WIDTH_MM * MM_TO_INCH * DPI)   # ~1011 px
H = int(CARD_HEIGHT_MM * MM_TO_INCH * DPI)  # ~638 px
BG = (240, 240, 240)

# ==== Helpers ====
def rnd_name():
    first = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Phan", "Vũ", "Đặng","Võ","Ngô","Đào"]
    middle = ["Văn", "Thị", "Minh", "Thu", "Quang", "Hữu", "Ngọc", "Thùy"]
    last = ["An", "Bảo", "Cường", "Dũng", "Hằng", "Huy", "Lan", "Linh", "Thiện", "Hồng","Quân","Hoàng","Phúc","Trung","Tuấn","Vy","Yến","Khoa","My","Như","Phương","Quỳnh","Thảo","Trang","Tuệ","Tùng","Thương","Tân"]
    return f"{random.choice(first)} {random.choice(middle)} {random.choice(last)}"


def to_ascii_filename(s: str) -> str:
    """Normalize a string to an ASCII-only, filesystem-safe filename fragment.

    Removes diacritics using unicode normalization, replaces whitespace with
    underscores, and strips unsafe characters.
    """
    import unicodedata
    import re

    # Decompose accents and remove combining marks
    nfkd = unicodedata.normalize('NFKD', s)
    without_accents = ''.join(c for c in nfkd if not unicodedata.combining(c))
    # Replace whitespace with underscore
    t = re.sub(r"\s+", "_", without_accents)
    # Remove any character that is not alphanumeric, underscore, dot or hyphen
    t = re.sub(r"[^A-Za-z0-9_.-]", '', t)
    # Collapse multiple underscores
    t = re.sub(r"_+", "_", t)
    # Trim leading/trailing separators
    return t.strip('_.-')

# ==== Generate random data theo quy ước ==== 
name = rnd_name()

# Random năm sinh (ví dụ trong khoảng 2000-2005 cho hợp lý)
year = random.randint(2000, 2005)
dob = f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{year}"

# Xác định Khóa học
khoa = year - 1986                # 2003 -> 17
nam_bd = 2004 + khoa        # K17 -> 2021
nam_kt = nam_bd + 4
course = f"{nam_bd} - {nam_kt}"

# Lớp
cls = f"DHTH{khoa}{random.choice(['A','B','C','D','E','F'])}"

# MSSV = 2 số cuối của năm bắt đầu học + 5 số random
prefix = str(nam_bd)[-2:]         # ví dụ 2021 -> '21'
student_code = prefix + f"{random.randint(10000, 99999)}"+"1"

# Hometown như cũ
hometown = random.choice([
    "Tỉnh Bình Phước", "Tỉnh Cà Mau", "Tỉnh Đồng Nai", "Tỉnh Tây Ninh",
    "Tỉnh Bạc Liêu", "Tỉnh Sóc Trăng", "Tỉnh Trà Vinh", "Tỉnh Vĩnh Long",
    "Tỉnh Long An", "Tỉnh An Giang", "Tỉnh Kiên Giang", "Tỉnh Hậu Giang",
    "Tỉnh Đồng Tháp", "Tỉnh Ninh Thuận", "Tỉnh Bình Thuận", "Tỉnh Khánh Hòa",
    "Tỉnh Phú Yên", "Tỉnh Quảng Nam", "Tỉnh Quảng Ngãi", "Tỉnh Bình Định",
    "Thành phố Đà Nẵng"
])


# ==== Create card base ====
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ==== Fonts ====
try:
    font_title = ImageFont.truetype("times.ttf", 48)
    font_name  = ImageFont.truetype("timesi.ttf", 40)
    font_info  = ImageFont.truetype("times.ttf", 32)
    font_code  = ImageFont.truetype("times.ttf", 36)
except Exception:
    font_title = font_name = font_info = font_code = ImageFont.load_default()

# ==== Logo ====
logo_path = None
for candidate in ["IUHLogo.png", "Logo.png", "logo.png"]:
    p = os.path.join(os.getcwd(), candidate)
    if os.path.exists(p):
        logo_path = p
        break

if logo_path:
    logo = Image.open(logo_path)
    try:
        logo = logo.resize((210, 150), Image.Resampling.LANCZOS)
    except Exception:
        logo = logo.resize((210, 150))
    img.paste(logo, (28, 20), logo if logo.mode == 'RGBA' else None)
else:
    draw.rectangle((28, 22, 140, 140), outline=(200, 200, 200))
    draw.text((36, 60), "IUH\nLogo", fill=(212,59,47), font=font_info)

# ==== Header text (phần phải logo) ====
x0, x1 = 210, W-40  # vùng text bên phải logo

def draw_centered_text_region(text, y, font, fill):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    x = x0 + (x1 - x0 - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)

line_height_header = 35  # giãn cách header

draw_centered_text_region("BỘ CÔNG THƯƠNG", 20, font_info, (32,58,138))
draw_centered_text_region("TRƯỜNG ĐẠI HỌC CÔNG NGHIỆP TP.HCM", 20 + line_height_header, font_info, (212,59,47))
draw_centered_text_region("12 Nguyễn Văn Bảo, P.4, Q. Gò Vấp, Tp.HCM", 20 + 2*line_height_header, font_info, (32,58,138))
draw_centered_text_region("...............................................................", 20 + 2.5*line_height_header, font_info, (0,0,0))

# ==== Student photo (dịch xuống) ====
photo_x, photo_y = 48, 200   # dịch xuống 20px
photo_w, photo_h = 180, 220

draw.rectangle((photo_x, photo_y, photo_x+photo_w, photo_y+photo_h), outline=(200,200,200), width=2)
student_photo_path = os.path.join(os.getcwd(), "student_photo.png")

try:
    student_photo = Image.open(student_photo_path)
    try:
        student_photo = student_photo.resize((photo_w, photo_h), Image.Resampling.LANCZOS)
    except Exception:
        student_photo = student_photo.resize((photo_w, photo_h))
    img.paste(student_photo, (photo_x, photo_y), student_photo if student_photo.mode=='RGBA' else None)
except Exception:
    draw.text((photo_x+12, photo_y+60), "Ảnh\nSV", fill=(212,59,47), font=font_info)

# ==== Thông tin bên phải ====
draw_centered_text_region("THẺ SINH VIÊN", 180, font_title, (32,58,138))
draw_centered_text_region(name, 240, font_name, (0,0,0))

start_y = 300
line_height = 50

draw.text((250, start_y), f"NS: {dob}", font=font_info, fill=(0,0,0))
draw.text((570, start_y), f"Lớp: {cls}", font=font_info, fill=(0,0,0))
draw.text((250, start_y + line_height), f"Khóa học: {course}", font=font_info, fill=(0,0,0))
draw.text((250, start_y + 2*line_height), f"HKTT: {hometown}", font=font_info, fill=(0,0,0))

# ==== Student code dưới ảnh ====
code_w = font_code.getbbox(student_code)[2] - font_code.getbbox(student_code)[0]
code_x = photo_x + (photo_w - code_w) // 2
code_y = photo_y + photo_h + 80  # tính theo vị trí mới
draw.text((code_x, code_y), student_code, font=font_code, fill=(0,0,0))
# ==== Barcode dưới thông tin bên phải ==== 
barcode_value = f"{student_code}_{cls}"  # ghép thêm tên + lớp để barcode dài hơn

code128 = barcode.get('code128', barcode_value, writer=ImageWriter())
barcode_bytes = BytesIO()
code128.write(
    barcode_bytes,
    options={
        "module_width": 0.25,
        "module_height": 9,  # tăng chiều cao để barcode rõ hơn
        "quiet_zone": 2,
        "write_text": False  # hiện số/chuỗi barcode bên dưới
    }
)
barcode_bytes.seek(0)
bar = Image.open(barcode_bytes)

bar_h = bar.height
bar_w = int(bar.width)

x0, x1 = 210, W-40
bar_x = x0 
bar_y = 470

available_w = x1 - bar_x
if available_w > 0 and bar_w != available_w:
    bar = bar.resize((available_w, bar_h), Image.Resampling.LANCZOS)
    bar_w = available_w
elif available_w <= 0:
    bar_x = x1 - bar_w

img.paste(bar, (bar_x, bar_y))


# ==== Save với tên file theo MSSV_HoTen ====
# Giả sử các biến name, student_code, img, dob, cls đã được định nghĩa trước

safe_name = to_ascii_filename(name)
output_dir = r"D:\DoAn\DataBip"
os.makedirs(output_dir, exist_ok=True)

OUTFILE = os.path.join(output_dir, f"{student_code}_{safe_name}.png")

img.save(OUTFILE)
print("Saved:", OUTFILE)
print("Student:", name, dob, cls, student_code)
