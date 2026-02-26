import cv2
import os
import time
from datetime import datetime
import mysql.connector

# ===== USER INPUT =====
total_minutes = float(input("Enter total recording duration (minutes): "))
interval_minutes = float(input("Enter clip interval (minutes): "))

total_seconds = total_minutes * 60
interval_seconds = interval_minutes * 60

# ===== MYSQL CONNECTION =====
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="video_recorder"
)

cursor = db.cursor()

# ===== CREATE RECORDINGS FOLDER =====
if not os.path.exists("recordings"):
    os.makedirs("recordings")

# ===== CAMERA SETUP =====
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

start_program_time = time.time()
clip_count = 1

while (time.time() - start_program_time) < total_seconds:
    
    clip_start_time = datetime.now()
    clip_filename = f"clip_{clip_count}.mp4"
    clip_path = os.path.join("recordings", clip_filename)
    
    out = cv2.VideoWriter(clip_path, fourcc, 20.0, (640,480))
    
    clip_start = time.time()
    
    while (time.time() - clip_start) < interval_seconds:
        ret, frame = cap.read()
        if not ret:
            break
        
        out.write(frame)
        cv2.imshow("Recording...", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    clip_end_time = datetime.now()
    duration = (clip_end_time - clip_start_time).total_seconds()
    
    out.release()
    
    sql = """
    INSERT INTO clips
    (clip_id, recording_date, start_time, end_time, duration_seconds, file_name, file_path)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        clip_count,
        clip_start_time.date(),
        clip_start_time,
        clip_end_time,
        int(duration),
        clip_filename,
        clip_path
    )
    
    cursor.execute(sql, values)
    db.commit()
    
    print(f"Saved clip {clip_count}")
    
    clip_count += 1

cap.release()
cv2.destroyAllWindows()
cursor.close()
db.close()

print("Recording completed successfully!")