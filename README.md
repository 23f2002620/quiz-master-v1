# Quiz Master v1

A multi-user exam preparation and quiz management platform built with Flask. This web app enables admins to create and manage subjects, chapters, quizzes, and questions while allowing users to register, attempt quizzes, and track their progress. Visualizations and a modern UI provide a comprehensive experience for both learners and administrators.

## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

### For Users
- User registration and login
- Browse available subjects, chapters, and quizzes
- Attempt quizzes and receive instant scores
- View quiz history and performance analytics (charts)
- Search for subjects and view quiz details

### For Admins
- Admin login and dashboard
- Create, edit, and delete subjects, chapters, quizzes, and questions
- Manage user accounts
- Visualize user and quiz performance with charts
- Search for users, subjects, and quizzes

## Demo

- **Live Project Link:** [Quiz Master v1 on GitHub](https://github.com/23f2002620/quiz-master-v1)
- **Demo Video:** [Google Drive Link](https://drive.google.com/file/d/1a2uSyIJhGFZub0x5M5AP0I6erawk0aN3/view)

## Getting Started

### Prerequisites

- Python 3.11.x
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/23f2002620/quiz-master-v1.git
   cd quiz-master-v1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the platform:**
   Open your browser and go to [http://localhost:5000](http://localhost:5000)

### Default Admin
- On first run, an admin account is created automatically:
  - **Username:** admin
  - **Password:** admin123

## Project Structure

```
quiz-master-v1/
│
├── app.py                # Main Flask application and routes
├── models.py             # SQLAlchemy ORM models
├── requirements.txt      # Python dependencies
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Main layout template
│   └── ...               # Other page templates
├── static/               # Static files (CSS, images)
└── README.md
```

## Usage

### User
- Register and log in as a user
- Browse and attempt available quizzes
- Review your scores and progress charts on your dashboard

### Admin
- Log in as admin (see credentials above)
- Add/edit/delete subjects, chapters, quizzes, questions, and users
- Review analytics and manage platform content

## Technologies Used

- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM for SQLite database
- **Werkzeug** - Secure password hashing
- **Matplotlib** - Visualization (charts for scores and analytics)
- **Bootstrap** - Responsive UI (via CDN)
- **Jinja2** - Template rendering

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## Contact

**Developer:** Saravanan  
**Email:** 23f2002620@ds.study.iitm.ac.in

---

*This project was developed as a course project for IITM Data Science.*
