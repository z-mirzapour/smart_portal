### README.md File
```markdown
# Smart Course Registration Portal

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.x-lightgrey)

A modern web application for university course registration with role-based access control.

## Key Features
- **Dual-Role System**:
  - Students: Browse/register for courses
  - Admins: Manage courses and view all enrollments
- **Smart Scheduling**: Conflict detection
- **JSON Database**: No SQL required
- **Responsive UI**: Works on all devices



## Project Structure
smart-portal/
├── app/
│   ├── templates/          
│   ├── static/             # CSS/JS/videos
│   ├── models/             # Data handling
│   ├── routes/             # View controllers
│   ├── services/
│   ├── utils/
│   ├── __init__.py         # Flask app creation
|   └── config.py           # Configuration
├── data/                   # JSON databases                 
├── run.py  
├── README.md
└── URL_DIAGRAM.md  
