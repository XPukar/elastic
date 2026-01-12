import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis

VIDEO_IN = "input.mp4"
VIDEO_OUT = "output.mp4"
THRESHOLD = 0.5
FRAME_SKIP = 3   # process every Nth frame (performance)

# --------------------
# Load face engine
# --------------------
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)

# --------------------
# Load enrolled faces
# --------------------
db = {}
for file in os.listdir("db"):
    if file.endswith(".npy"):
        name = file.replace(".npy", "")
        db[name] = np.load(f"db/{file}")

print(f"Loaded {len(db)} enrolled identities")

# --------------------
# Open video
# --------------------
cap = cv2.VideoCapture(VIDEO_IN)
if not cap.isOpened():
    raise RuntimeError("Cannot open video file")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer = cv2.VideoWriter(
    VIDEO_OUT,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

frame_id = 0

# --------------------
# Process frames
# --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # Skip frames for performance
    if frame_id % FRAME_SKIP != 0:
        writer.write(frame)
        continue

    faces = app.get(frame)

    for face in faces:
        emb = face.normed_embedding

        best_name = "UNKNOWN"
        best_score = 0.0

        for name, ref_emb in db.items():
            score = float(np.dot(emb, ref_emb))
            if score > best_score:
                best_score = score
                best_name = name

        if best_score < THRESHOLD:
            best_name = "UNKNOWN"

        box = face.bbox.astype(int)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

        label = f"{best_name} {best_score:.2f}"
        cv2.putText(
            frame,
            label,
            (box[0], box[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    writer.write(frame)

cap.release()
writer.release()

print("Video processing complete → output.mp4")
