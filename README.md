# Face Recognition Attendance System

A modern face recognition attendance system built with FastAPI, PostgreSQL, Vue.js, and face_recognition library.

## Features

- **Person Management**: Register persons with face images, update details and photos
- **Face Recognition**: Identify persons from uploaded images or webcam capture
- **Attendance Tracking**: Mark attendance via face recognition with duplicate prevention
- **Real-time Detection**: Continuous face scanning for hands-free attendance
- **Reports**: View and export attendance records by date

## Tech Stack

**Backend**
- FastAPI - REST API framework
- PostgreSQL - Database with face encodings
- face_recognition - Face detection and recognition
- OpenCV - Image processing

**Frontend**
- Vue.js 3 + TypeScript
- Vite - Build tool
- Axios - HTTP client

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL
- Node.js 18+

### Installation

1. **Clone and setup environment**
```bash
git clone <repository-url>
cd FaceRecognition
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure database**
```bash
# Create PostgreSQL database
createdb facialRecognition

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
```

3. **Run database migration**
```bash
python database/run_migration.py
```

4. **Start backend**
```bash
python backend/main.py
# API runs at http://localhost:8000
# Docs at http://localhost:8000/docs
```

5. **Start frontend** (new terminal)
```bash
cd frontend/user-interface
npm install
npm run dev
# App runs at http://localhost:5173
```

## Project Structure

```
FaceRecognition/
├── backend/
│   ├── api/              # API routes and dependencies
│   ├── config/           # Application settings
│   ├── models/           # Pydantic schemas
│   ├── services/         # Business logic
│   └── utils/            # Helper functions
├── database/
│   ├── repositories/     # Data access layer
│   ├── db.py            # Connection pooling
│   └── schema.sql       # Database schema
├── frontend/
│   └── user-interface/  # Vue.js application
└── .env                 # Configuration (create from .env.example)
```

## API Endpoints

### Persons
- `POST /api/v1/persons/` - Create person
- `GET /api/v1/persons/` - List all persons
- `GET /api/v1/persons/{id}` - Get person details
- `PUT /api/v1/persons/{id}` - Update person
- `DELETE /api/v1/persons/{id}` - Delete person
- `GET /api/v1/persons/{id}/image` - Get person image
- `PUT /api/v1/persons/{id}/image` - Update person image

### Face Recognition
- `POST /api/v1/face-recognition/upload` - Register person with image
- `POST /api/v1/face-recognition/recognize` - Identify face

### Attendance
- `POST /api/v1/attendance/mark` - Mark attendance (manual)
- `POST /api/v1/attendance/mark/face` - Mark via face recognition
- `GET /api/v1/attendance/today` - Today's attendance
- `GET /api/v1/attendance/date/{date}` - Attendance by date
- `GET /api/v1/attendance/person/{id}` - Person's attendance history
- `GET /api/v1/attendance/export/today` - Export today's CSV
- `GET /api/v1/attendance/export/date/{date}` - Export CSV by date

## Configuration

Edit `.env` file:

```env
# Database
DB_NAME=facialRecognition
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# API
API_PREFIX=/api/v1
ALLOWED_ORIGINS=http://localhost:5173

# Face Recognition
FACE_DETECTION_MODEL=hog  # 'hog' (faster) or 'cnn' (accurate)
FACE_RECOGNITION_TOLERANCE=0.6  # Lower = stricter matching
```

## Development

**Backend**
```bash
# Run with hot reload
uvicorn backend.main:app --reload

# Run tests (if available)
pytest
```

**Frontend**
```bash
cd frontend/user-interface

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## License

MIT
