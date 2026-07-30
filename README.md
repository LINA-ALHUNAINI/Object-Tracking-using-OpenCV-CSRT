# Object Tracking with OpenCV

A real-time object tracking project built with OpenCV’s CSRT tracker. The user selects
an object through the webcam feed, and the algorithm tracks it live across frames.

## Demo

`![demo](objectTracking.gif)`)*

## How It Works

1. The camera opens and shows a live preview window.
1. Press **SPACE** or **ENTER** to capture the current frame.
1. Drag a box around the object you want to track, then press **ENTER**.
1. The tracker follows the object in real time, drawing a green box around it
   and showing the live FPS.
1. If the object is lost (moves out of frame, gets covered, etc.), the video
   keeps playing normally and a red “Lost” message appears — tracking does
   **not** resume automatically.
1. Controls:
- **r** → manually re-select a new object at any time
- **q** → quit the program

## Why Manual Re-selection Instead of Automatic?

Early versions of this project tried automatically reopening the selection
window whenever the object was lost for too long. In practice this was
disruptive — it interrupted the live video even for a brief, momentary loss.
The tracker was changed to stay passive on loss (just showing “Lost”) and
let the user decide when to re-select with **r**, which gives a much smoother
experience.

## Setup

1. Install [Anaconda](https://www.anaconda.com/download) and
   [VS Code](https://code.visualstudio.com/download).
1. Create and activate a dedicated environment:
   
   ```
   conda create -n cvproject python=3.10
   conda activate cvproject
   ```
1. Install the required libraries:
   
   ```
   pip install -r requirements.txt
   ```

## Running the Project

```
python object_tracking.py
```

## Limitations

- CSRT tracking has no built-in re-detection: once the object is lost, it
  will not automatically reappear in tracking mode even if it comes back
  into frame — the user must press **r**.
- Tracking accuracy drops with very fast motion or significant lighting changes.
- Only one object is tracked at a time.

## Tech Used

- Python 3.10
- OpenCV (`opencv-contrib-python`) — `cv2.legacy.TrackerCSRT_create()`

-----

# تتبُّع الأجسام باستخدام OpenCV

مشروع لتتبُّع الأجسام في الوقت الفعلي يعتمد على خوارزمية CSRT من مكتبة OpenCV. يقوم
المستخدم بتحديد جسم معيّن عبر كاميرا الويب، وتتولى الخوارزمية تتبُّعه بشكل مستمر عبر
الإطارات (Frames).

## عرض توضيحي (Demo)
`![demo](objectTracking.gif)`)*

## آلية عمل المشروع

1. تُفتح الكاميرا وتُعرض نافذة معاينة مباشرة.
1. يُضغط زر **SPACE** أو **ENTER** لالتقاط الإطار الحالي.
1. يُرسم مربع حول الجسم المراد تتبُّعه باستخدام الفأرة، ثم يُضغط زر **ENTER**.
1. تتولى الخوارزمية تتبُّع الجسم في الوقت الفعلي، مع رسم مربع أخضر حوله وعرض معدّل
   الإطارات (FPS) بشكل مستمر.
1. في حال فقدان الجسم (خروجه من الإطار، أو تغطيته، أو غير ذلك)، يستمر عرض الفيديو
   بشكل طبيعي مع ظهور رسالة حمراء بعبارة “Lost”، دون استئناف التتبُّع تلقائياً.
1. أزرار التحكم:
- **r** ← لإعادة تحديد جسم جديد يدوياً في أي وقت
- **q** ← للخروج من البرنامج

## سبب اختيار إعادة التحديد اليدوي بدلاً من التلقائي

اعتمدت النسخ الأولى من المشروع على إعادة فتح نافذة التحديد تلقائياً كلما فُقد الجسم
لفترة طويلة، غير أن هذا الأسلوب تبيّن أنه يسبّب إزعاجاً عملياً، إذ كان يقاطع عرض
الفيديو المباشر حتى في حالات الفقدان اللحظي البسيط. لذلك، جرى تعديل الخوارزمية لتبقى
في حالة سكون عند فقدان الجسم (تكتفي بعرض عبارة “Lost”)، وتُركت عملية إعادة التحديد
لتقدير المستخدم عبر الضغط على زر **r**، وهو ما يمنح تجربة استخدام أكثر سلاسة.

## إعداد بيئة العمل

1. تثبيت [Anaconda](https://www.anaconda.com/download) و [VS Code](https://code.visualstudio.com/download).
1. إنشاء بيئة خاصة بالمشروع وتفعيلها:
   
   ```
   conda create -n cvproject python=3.10
   conda activate cvproject
   ```
1. تثبيت المكتبات المطلوبة:
   
   ```
   pip install -r requirements.txt
   ```

## تشغيل المشروع

```
python object_tracking.py
```

## القيود (Limitations)

- لا تتضمّن خوارزمية CSRT آلية لإعادة الاكتشاف التلقائي؛ فبمجرد فقدان الجسم، لا
  يُستأنف تتبُّعه تلقائياً حتى لو عاد إلى الإطار، ويتطلّب الأمر ضغط زر **r** يدوياً.
- تنخفض دقّة التتبُّع مع الحركة السريعة جداً أو التغيّرات الكبيرة في الإضاءة.
- يقتصر المشروع على تتبُّع جسم واحد في الوقت نفسه.

## التقنيات المستخدمة

- Python 3.10
- OpenCV (`opencv-contrib-python`) — `cv2.legacy.TrackerCSRT_create()`
