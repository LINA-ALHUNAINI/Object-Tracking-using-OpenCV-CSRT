"""
Object Tracking Project - OpenCV
Tracks a moving object through the webcam feed using the CSRT algorithm.

الفكرة (Concept):
1. المستخدم يحدد الجسم المراد تتبعه بأول فريم (بالماوس) - user selects the object in the first frame
2. الخوارزمية تتنبأ بموقعه في كل فريم لاحق بدل ما تعيد اكتشافه من الصفر
   The algorithm predicts its location in each following frame instead of re-detecting from scratch
3. نرسم صندوق حول الموقع الجديد ونعرض FPS لحظياً - draw a box around the new location and show live FPS
4. لو انفقد الجسم لمدة طويلة، تفتح نافذة اختيار جديدة تلقائياً لإعادة تحديده
   If the object stays lost for too long, a new selection window opens automatically to re-pick it

المتطلبات (Requirements):
- opencv-contrib-python (يحتوي وحدة cv2.legacy التي فيها الـ Trackers)
"""

import cv2
import time

# عدد الفريمات المتتالية اللي نسمح فيها بضياع الجسم قبل إعادة التحديد تلقائياً
# Number of consecutive "lost" frames allowed before triggering auto re-selection
LOST_THRESHOLD = 30  # roughly 1 second at ~30 FPS


def select_object(cap):
    """
    تفتح نافذة لاختيار الجسم من فريم جديد وتنشئ Tracker جديد له
    Opens a selection window on a fresh frame and creates a new tracker for it.
    تكرر المحاولة تلقائياً لو المستخدم ضغط Enter بدون ما يسحب مربع صحيح
    Retries automatically if the user presses Enter without dragging a valid box.
    """
    ret, frame = cap.read()
    if not ret:
        return None, None

    while True:
        print("Select the object by DRAGGING a box around it first, then press Enter or Space.")
        bbox = cv2.selectROI("Select Object - Press Enter", frame, False)

        x, y, w, h = bbox
        # نتأكد إن المربع فعلاً له حجم (مو نقطة أو صفر) - make sure the box actually has a size
        if w > 0 and h > 0:
            cv2.destroyWindow("Select Object - Press Enter")
            break
        print("No valid box was drawn. Please drag a box around the object before pressing Enter.")

    try:
        tracker = cv2.legacy.TrackerCSRT_create()
        tracker.init(frame, bbox)
    except cv2.error as e:
        print(f"Tracker init failed: {e}")
        return None, None

    return tracker, bbox


def main():
    # فتح كاميرا الويب (0 = الكاميرا المدمجة الافتراضية) - open webcam (0 = default built-in camera)
    # cv2.CAP_DSHOW يحل مشكلة الشاشة السوداء الشائعة على Windows
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open the camera. Make sure it isn't used by another app.")
        return

    tracker, bbox = select_object(cap)
    if tracker is None:
        print("Error: Could not read a frame from the camera.")
        cap.release()
        return

    prev_time = time.time()
    lost_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # تحديث موقع الجسم بهذا الفريم بناءً على الفريمات السابقة - update the object's location for this frame
        success, bbox = tracker.update(frame)

        # حساب FPS (عدد الفريمات بالثانية) لمعرفة سرعة الأداء - calculate FPS to measure performance
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
        prev_time = curr_time

        if success:
            # الجسم موجود، نصفّر عداد الضياع - object found, reset the lost counter
            lost_counter = 0
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            lost_counter += 1
            cv2.putText(frame, f"Lost ({lost_counter}/{LOST_THRESHOLD})", (50, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            # لو الجسم ضايع لمدة طويلة، نفتح نافذة اختيار جديدة تلقائياً
            # If the object has been lost for too long, trigger automatic re-selection
            if lost_counter > LOST_THRESHOLD:
                cv2.imshow("Object Tracking - Press q to quit", frame)
                cv2.waitKey(1)
                print("Object lost for too long. Please re-select it.")
                tracker, bbox = select_object(cap)
                if tracker is None:
                    break
                lost_counter = 0
                continue

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Object Tracking - Press q to quit", frame)

        # الخروج بالضغط على حرف q - quit by pressing q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
