import cv2
import sys
import json  # <- Thêm thư viện json
from pyzxing import BarCodeReader

# --- Khởi tạo ---
reader = BarCodeReader()
# Mở webcam mặc định
cap = cv2.VideoCapture(0)

# Kiểm tra webcam có mở được không
if not cap.isOpened():
    # Nếu lỗi, trả về một đối tượng JSON chứa thông báo lỗi
    error_message = json.dumps({"status": "error", "message": "Không thể mở webcam."})
    print(error_message)
    sys.exit()

print("🚀 Webcam đã sẵn sàng. Đưa mã vào camera...")
print("   (Nhấn 'q' trên cửa sổ video để thoát)")

# --- Vòng lặp chính ---
while True:
    # Đọc từng khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        print(json.dumps({"status": "error", "message": "Không nhận được khung hình."}))
        break

    # Giải mã mã vạch/QR từ khung hình
    results = reader.decode_array(frame)

    # --- XỬ LÝ VÀ TRẢ VỀ JSON ---
    if results:
        # 1. Chuẩn bị một danh sách (list) để chứa thông tin các mã nhận dạng được
        detected_codes = []
        for result in results:
            # 2. Với mỗi mã, tạo một đối tượng (dictionary) chứa thông tin
            code_info = {
                "mssv": result.get('raw', b'').decode('utf-8', 'ignore')
            }
            # Thêm đối tượng này vào danh sách
            detected_codes.append(code_info)

        # 3. Chuyển đổi toàn bộ danh sách thành một chuỗi JSON
        # indent=2 để JSON hiển thị đẹp mắt hơn
        # ensure_ascii=False để hiển thị đúng tiếng Việt
        json_output = json.dumps(detected_codes, indent=2, ensure_ascii=False)

        # 4. In chuỗi JSON ra console
        print(json_output)

    # Hiển thị cửa sổ video (bạn có thể bỏ phần này nếu chỉ cần chạy ngầm)
    cv2.imshow('Real-time Scanner - Press Q to quit', frame)

    # Thoát nếu nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("...Đã thoát chương trình.")
        break

# --- Dọn dẹp ---
cap.release()
cv2.destroyAllWindows()