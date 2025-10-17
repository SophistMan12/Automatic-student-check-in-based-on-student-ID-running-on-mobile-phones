import cv2
import sys  # Thêm thư viện sys để thoát chương trình một cách an toàn
from pyzxing import BarCodeReader

# Khởi tạo reader
reader = BarCodeReader()

# --- PHẦN SỬA LỖI ---

# 1. Dùng raw string r"..." để tránh lỗi đường dẫn trong Windows
image_path = r"dataset/images/train/22975681_Phan_Van_Thien.png"

# 2. Đọc ảnh
img = cv2.imread(image_path)

# 3. KIỂM TRA QUAN TRỌNG: Đảm bảo ảnh đã được tải thành công
if img is None:
    print(f"❌ Lỗi: Không thể đọc được file ảnh tại đường dẫn: {image_path}")
    print("   Vui lòng kiểm tra lại đường dẫn có chính xác không và file ảnh có tồn tại không.")
    sys.exit() # Thoát chương trình nếu không có ảnh

# --- TỐI ƯU HÓA CODE ---

# 4. Thay vì lưu file tạm, hãy decode trực tiếp từ mảng numpy của ảnh
#    Việc này nhanh hơn và không tạo ra file rác.
#    Hàm decode_array được thiết kế cho việc này.
result = reader.decode_array(img)

# In kết quả
if result:
    print("✅ Đã đọc mã thành công:")
    # result có thể là một danh sách nếu có nhiều mã trong ảnh
    for r in result:
        # Kiểm tra xem các key có tồn tại không trước khi truy cập
        barcode_type = r.get('type', 'N/A')
        barcode_data = r.get('raw', b'').decode('utf-8') # Decode byte sang string
        print(f"- Loại mã: {barcode_type}, Dữ liệu: {barcode_data}")
else:
    print("❌ Không phát hiện được mã vạch/QR code trong ảnh.")