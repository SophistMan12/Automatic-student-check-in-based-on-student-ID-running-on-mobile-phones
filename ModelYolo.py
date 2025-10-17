# test_image_yolo_resize.py
import cv2
from ultralytics import YOLO

# 1. Load model
model = YOLO(r"D:\DoAn\dataset\runs\detect\train5\weights\best.pt")

# 2. Load ảnh
image_path = r"D:\DoAn\imagetest.jpg"
img = cv2.imread(image_path)

# 3. Resize ảnh để hiển thị dễ nhìn (ví dụ max width 800)
max_width = 800
height, width = img.shape[:2]
if width > max_width:
    scale = max_width / width
    img = cv2.resize(img, (int(width*scale), int(height*scale)))

# 4. Dự đoán
results = model(img)

# 5. Vẽ bounding boxes
for r in results:
    for box in r.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        cls = int(box.cls[0])
        label = f"{cls} {conf:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 6. Hiển thị ảnh
cv2.imshow("YOLO Detection (Resized)", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
