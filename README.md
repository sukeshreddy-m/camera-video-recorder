Camera Video Recorder (Python + MySQL)
This project records video from the system camera for a given total duration and creates clips at given time intervals.  
Each clip is saved in a `recordings/` folder and its details are stored in a MySQL database.

How It Works
- User enters total recording duration (in minutes)
- User enters clip interval (in minutes)
- The camera runs for the total duration
- A new video clip is created at each interval
- Metadata of each clip is stored in MySQL

Technologies Used
- Python
- OpenCV
- MySQL
- mysql-connector-python

Database Schema
```sql
CREATE DATABASE video_recorder;

USE video_recorder;

CREATE TABLE clips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clip_id INT,
    recording_date DATE,
    start_time DATETIME,
    end_time DATETIME,
    duration_seconds INT,
    file_name VARCHAR(255),
    file_path VARCHAR(500)
);
```

Setup Instructions
1. Install required packages: pip install opencv-python mysql-connector-python
2. Start MySQL server.
3. Create the database and table using the schema above.
4. Run the program:main.py
5. Enter total duration and interval when prompted.

Assumptions
- Default system camera is used.
- MySQL is running locally.
- Root user has no password (for local testing).

Sukesh Reddy