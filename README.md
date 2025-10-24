# CollegeScrap 🎓

**"Know your degree requirements in 30 seconds. Be ready for your advisor meeting in 2 minutes."**

CollegeScrap is a web application that scrapes Ole Miss catalog data, calculates exactly what you need to graduate, and generates a balanced semester-by-semester schedule you can bring to your advisor meeting.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)

## Features

- **Instant Degree Analysis**: Upload your major, minor, and classification to see all degree requirements in 30 seconds
- **Smart Schedule Generation**: Get balanced semester schedules that respect prerequisites and workload
- **Prerequisite Chain Detection**: Identify critical courses that unlock many others
- **Workload Balancing**: Avoid overloading yourself with too many heavy courses
- **Export for Advisors**: Download your schedule as a text file for advisor meetings
- **Real-time Catalog Data**: Scrapes Ole Miss catalog to ensure up-to-date information

## Tech Stack

### Backend
- **Python 3.8+** - Core backend language
- **Flask** - Web framework for REST API
- **SQLAlchemy** - Database ORM
- **BeautifulSoup4** - Web scraping Ole Miss catalog
- **SQLite** - Lightweight database for storing course data

### Frontend
- **React 18** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **CSS3** - Modern, responsive styling

## Project Structure

```
college-scrap/
├── backend/                    # Flask backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes.py      # Endpoint definitions
│   │   ├── models/            # Database models
│   │   │   └── database.py    # SQLAlchemy models
│   │   ├── scrapers/          # Web scrapers
│   │   │   └── catalog_scraper.py
│   │   ├── utils/             # Utility functions
│   │   │   ├── degree_analyzer.py
│   │   │   └── scheduler.py
│   │   └── __init__.py        # Flask app factory
│   ├── requirements.txt       # Python dependencies
│   ├── run.py                 # Application entry point
│   └── .env.example           # Environment variables template
│
├── frontend/                  # React frontend
│   ├── public/               # Static files
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   │   ├── DegreeSelection.js
│   │   │   ├── RequirementsResults.js
│   │   │   ├── ScheduleBuilder.js
│   │   │   └── GeneratedSchedule.js
│   │   ├── services/         # API service
│   │   │   └── api.js
│   │   ├── styles/           # CSS files
│   │   ├── App.js            # Main app component
│   │   └── index.js          # Entry point
│   └── package.json          # Node dependencies
│
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/college-scrap.git
   cd college-scrap
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python -c "from app.models.database import init_db; init_db()"
   ```

6. **Populate database with sample data**
   ```bash
   python -m app.scrapers.catalog_scraper
   ```

7. **Run the Flask server**
   ```bash
   python run.py
   ```

   The backend will be running at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the React development server**
   ```bash
   npm start
   # or
   yarn start
   ```

   The frontend will be running at `http://localhost:3000`

## Usage

1. **Select Your Degree** (Step 1)
   - Choose your major (e.g., Computer Science)
   - Select degree type (B.S. or B.A.)
   - Optionally add a minor
   - Select your current classification

2. **View Requirements** (Step 2)
   - See total credit breakdown
   - Review all required courses
   - Identify important prerequisite chains

3. **Build Schedule** (Step 3)
   - Choose target semester
   - Select credit load preference
   - Mark completed courses

4. **Get Balanced Schedule** (Step 4)
   - Review recommended courses
   - Check workload warnings
   - Download for advisor meeting

## API Endpoints

### GET /api/health
Health check endpoint

### GET /api/majors
Get all available majors

### GET /api/minors
Get all available minors

### POST /api/degree-requirements
Get degree requirements analysis
```json
{
  "major_id": 1,
  "minor_id": 2,
  "classification": "Freshman"
}
```

### POST /api/generate-schedule
Generate a semester schedule
```json
{
  "major_id": 1,
  "minor_id": 2,
  "semester": "Fall 2025",
  "credit_load": "standard",
  "completed_courses": ["CSCI 111", "MATH 261"]
}
```

### GET /api/courses/{course_code}
Get details for a specific course

## Database Schema

### Course
- `id`: Primary key
- `code`: Course code (e.g., "CSCI 111")
- `name`: Course name
- `credits`: Credit hours
- `description`: Course description
- `workload`: Light/Moderate/Heavy
- `category`: Core/GenEd/Elective

### Major
- `id`: Primary key
- `name`: Major name
- `degree_type`: B.S./B.A./etc.
- `total_credits`: Total credits required
- `major_credits`: Credits for major courses

### Minor
- `id`: Primary key
- `name`: Minor name
- `required_credits`: Total credits required

### GenEdRequirement
- `id`: Primary key
- `category`: GenEd category
- `required_credits`: Credits required
- `description`: Description

## Deployment

### Option 1: Vercel (Frontend) + PythonAnywhere (Backend)

**Frontend (Vercel)**
```bash
cd frontend
npm run build
vercel deploy
```

**Backend (PythonAnywhere)**
1. Upload backend code to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI file to point to `run.py`
4. Set environment variables in web app settings

### Option 2: AWS EC2 (All-in-One)

1. **Launch EC2 instance** (Ubuntu 22.04)

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx nodejs npm
   ```

3. **Set up backend**
   ```bash
   cd backend
   pip3 install -r requirements.txt
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

4. **Build and serve frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   sudo cp -r build/* /var/www/html/
   ```

5. **Configure Nginx** as reverse proxy

### Option 3: Railway (Quick Deploy)

1. Connect GitHub repo to Railway
2. Add two services: `backend` and `frontend`
3. Set environment variables
4. Deploy automatically on git push

## Environment Variables

### Backend (.env)
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///collegescrap.db
CATALOG_BASE_URL=https://catalog.olemiss.edu
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Future Enhancements

- [ ] Add more majors and minors
- [ ] Implement actual web scraping for Ole Miss catalog
- [ ] Add course ratings/difficulty from RateMyProfessor
- [ ] Email schedule directly to student/advisor
- [ ] PDF export with prettier formatting
- [ ] 4-year plan generator
- [ ] Course substitution suggestions
- [ ] Mobile app version
- [ ] Support for other universities

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ole Miss Academic Catalog
- Flask and React communities
- All contributors who helped build this tool

## Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ to help students graduate on time
