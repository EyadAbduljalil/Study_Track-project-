
# **StudyTrack Final Project**

#### Video Demo: [Insert Video URL Here]

### **Description:**
The **StudyTrack** project is a personal task management web application designed to help students track their study progress, tasks, and deadlines. This project integrates features such as user authentication, profile management, task creation, filtering tasks by status and priority, and viewing course progress.

The project uses **Flask** for the backend, **HTML/CSS** for the frontend, and **SQLAlchemy** to interact with the database. The user interface is designed to be responsive, using **Bootstrap** for a smooth and clean design. The application also allows users to update their profiles, upload a profile picture, and track their completed tasks.

**Features of the Application:**
- **User Registration and Authentication**: Users can create accounts, log in, and manage their sessions securely.
- **Task Management**: Users can create, update, delete, and filter tasks based on their status (pending, in progress, completed) and priority (low, medium, high).
- **Profile Management**: Users can update their profile information, including username, email, password, and profile picture.
- **Statistics**: Users can view how many tasks they have completed and their last activity.

**Files and Their Functions:**
1. **app.py**: Contains the routes for managing tasks, courses, and user profiles. Handles the main logic of the application.
2. **models.py**: Defines the database models for the application (User, Task, and Course).
3. **templates/**: Contains the HTML templates for the pages of the application (home, login, registration, profile, tasks, etc.).
4. **static/**: Contains static files like images, CSS styles, and JavaScript.
5. **forms/**: Includes form classes for user input, such as **LoginForm**, **RegistrationForm**, and **ProfileForm**.
6. **README.md**: This file, which describes the project, its features, and how to set it up.

### **Development:**
This project was built using the **Flask** web framework. The backend uses **Flask-SQLAlchemy** for interacting with a **SQLite** database, and the frontend is designed using **HTML5**, **CSS3**, and **Bootstrap**.

### **Help and Contributions:**
Although this project was mainly developed by me, I did seek some minimal assistance from external resources. Specifically, I asked for help in creating and organizing my profile page functionality, ensuring it integrated seamlessly with the rest of the application. The **profile update** feature was a challenging part, and the guidance helped me implement it properly.

I also used **AI tools** like ChatGPT to help with debugging, code structure, and ideas for improving certain parts of the app, but all the core coding, design, and functionality were created by me.

### **Tools Used:**
- **Flask**: Backend web framework.
- **SQLAlchemy**: ORM for database management.
- **HTML/CSS/Bootstrap**: Frontend technologies.
- **SQLite**: Database management system.
- **GitHub**: For version control and project management.

### **Challenges Faced:**
- Integrating user authentication and task filtering.
- Ensuring the application remained responsive and worked well on mobile devices.
- Managing state between different user sessions effectively.

### **Future Enhancements:**
- Adding a **notification system** for task deadlines.
- Enhancing the **profile page** with additional features like changing the bio or adding links to other social media profiles.
- Implementing **user roles** (such as Admin) for better task management across teams.
