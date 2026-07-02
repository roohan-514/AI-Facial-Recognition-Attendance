# 🔥 AI Facial Recognition Attendance System

AI-powered attendance system using facial recognition for automated, contactless check-ins. This system provides real-time facial detection, recognition, and automated attendance marking with database integration.

## 🛠️ Tech Stack
- **Python** - Backend & Core Logic
- **OpenCV** - Computer Vision & Image Processing
- **Face Recognition Library** - Facial detection and recognition
- **NumPy & Pandas** - Data processing
- **Flask/FastAPI** - Web API (optional)
- **SQLite/PostgreSQL** - Attendance Database

## 📋 Features
✅ Real-time facial recognition from webcam feed
✅ Automated attendance marking
✅ Contactless check-in system
✅ Multi-person detection and tracking
✅ Database integration for attendance records
✅ Attendance reports and analytics
✅ Unknown face detection and alerts
✅ CSV export functionality

## 📁 Project Structure
```
AI-Facial-Recognition-Attendance/
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── src/
│   ├── face_recognition_system.py
│   ├── attendance_manager.py
│   └── __init__.py
├── known_faces/
│   └── (store registered face encodings)
├── data/
│   └── attendance.db
└── logs/
    └── attendance.log
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or camera access
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/roohan-514/AI-Facial-Recognition-Attendance.git
cd AI-Facial-Recognition-Attendance
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## 📦 Dependencies
```
opencv-python==4.8.0.76
face-recognition==1.3.5
face-recognition-models==0.3.0
numpy==1.24.3
pandas==2.0.3
pillow==10.0.0
scikit-learn==1.3.0
flask==2.3.3
```

## 🎯 Quick Start

### 1. Run the System
```bash
python main.py
```

### 2. Register Known Faces
- Follow the prompts to add employee names
- Capture multiple face angles for better recognition
- Encodings will be saved automatically

### 3. Start Attendance System
- Webcam feed will open
- Recognized faces will show green with name
- Unknown faces will show red with "Unknown"
- Attendance will be marked automatically

### 4. View Attendance Records
```bash
python src/generate_report.py --date 2024-01-15
```

## 💻 Usage Examples

### Basic Attendance Marking
```python
from src.face_recognition_system import FaceRecognitionSystem
from src.attendance_manager import AttendanceManager
from datetime import datetime

# Initialize
recognizer = FaceRecognitionSystem()
attendance = AttendanceManager()

# Recognize faces from webcam
results = recognizer.recognize_faces(frame)

# Mark attendance
attendance.mark_attendance(name="John Doe", confidence=0.95)
```

### Export Attendance Report
```bash
python src/attendance_manager.py --export csv --output attendance_report.csv
```

## 🎬 How It Works

1. **Face Registration**: Capture multiple angles of employee faces and generate encodings
2. **Real-time Detection**: OpenCV detects faces in the webcam feed
3. **Face Recognition**: Compare detected faces with registered encodings
4. **Attendance Marking**: Automatically log attendance with timestamp
5. **Database Storage**: Store records in SQLite
6. **Report Generation**: Generate daily/weekly/monthly attendance reports

## 🔐 Security Features
- Face encodings stored locally (not images)
- Unknown face detection and logging
- Duplicate attendance prevention (within 5 minutes)
- Secure database storage
- Access logs and audit trails

## 📊 Database Schema
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    confidence REAL,
    status TEXT DEFAULT 'Present'
);
```

## 🚨 Troubleshooting

### Issue: "No module named 'face_recognition'"
```bash
pip install face-recognition
pip install face-recognition-models
```

### Issue: Webcam not detected
- Check if camera is connected
- Verify camera permissions
- Try: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`

### Issue: Low recognition accuracy
- Register more face angles (up, down, left, right)
- Improve lighting conditions
- Increase face sample count (5-10 images per person)

## 📈 Performance Optimization
- Use GPU acceleration with CUDA for faster processing
- Optimize face encoding size (128D vectors)
- Implement face detection caching
- Multi-threading for real-time processing

## 🔄 Keyboard Controls
- **'q'** - Quit the application
- **'r'** - Register new face
- **'s'** - Capture face image (during registration)

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.

## 📧 Contact & Support
- **GitHub**: [@roohan-514](https://github.com/roohan-514)
- **Issues**: Report bugs via GitHub Issues

## 🎯 Future Enhancements
- [ ] Web dashboard for attendance management
- [ ] Mobile app integration
- [ ] Email/SMS notifications
- [ ] Advanced analytics and predictions
- [ ] Integration with HR systems
- [ ] Multi-location support
- [ ] Liveness detection (prevent spoofing)
- [ ] Real-time alerts for unauthorized access

---

**Status**: 🚀 Production Ready

**Last Updated**: 2024

**Maintained By**: [@roohan-514](https://github.com/roohan-514)
