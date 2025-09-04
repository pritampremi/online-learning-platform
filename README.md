# 🎓 Online Learning Platform  

A **Django-based Online Learning Platform** designed to simulate a real-world e-learning system. It provides separate role-based dashboards for **students, instructors, and admins**, with course management, enrollment, and quizzes.  

---

## ✨ Features  

### 👨‍🏫 Instructor  
- Create and manage courses & lessons  
- Create quizzes with multiple-choice questions  
- Track student quiz attempts & results  

### 🎓 Student  
- Browse and enroll in courses  
- Track learning progress  
- Attempt quizzes with multiple attempts allowed  
- View detailed results after submission  

### ⚙️ Admin  
- Manage users, courses, and system settings  

---

## 🛠️ Tech Stack  
- **Backend**: Django, Python  
- **Frontend**: HTML, CSS, Bootstrap (or Tailwind if used)  
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL  
- **Authentication**: Django built-in auth with role-based access  
- **Other Tools**: Django Forms, ModelForms, Class-based & function-based views  

---

## 🚀 How to Run Locally  

1. Clone the repo  
   ```bash
   git clone https://github.com/your-username/online-learning-platform.git
   cd online-learning-platform
   ```

2. Create & activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate   # (Linux/Mac)
   venv\Scripts\activate      # (Windows)
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations  
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (for admin access)  
   ```bash
   python manage.py createsuperuser
   ```

6. Run the server  
   ```bash
   python manage.py runserver
   ```

7. Open in browser  
   ```
   http://127.0.0.1:8000/
   ```

---

## 👤 Author  
**Pritam Premi**  
- 💼 [LinkedIn](https://linkedin.com/in/pritam-premi/)  

