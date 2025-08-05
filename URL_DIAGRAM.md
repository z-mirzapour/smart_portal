# Smart Portal URL Map

## Authentication Routes
├── /login (GET/POST) - User login
├── /register (GET/POST) - New user registration
└── /logout - Session termination

## Student Routes
├── /student/dashboard - Course overview
├── /student/courses - Available courses list
├── /student/register/<course_id> (POST) - Enroll in course
└── /student/schedule - Personal timetable

## Admin Routes
├── /admin/dashboard - System overview
├── /admin/courses - Course management (CRUD)
│ ├── /admin/courses/add (GET/POST) - Add new course
│ ├── /admin/courses/edit/<id> (GET/POST) - Modify course
│ └── /admin/courses/delete/<id> (POST) - Remove course
└── /admin/schedules - View all enrollments