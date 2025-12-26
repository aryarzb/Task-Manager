1- Project Name Task Manager (Python CLI)

2- Project Description This is a command-line Task Manager application written in Python. The project was built as a learning exercise to practice clean code, object-oriented programming, modular design, and working with time-based features such as reminders and timers.

The application allows users to manage tasks, set reminders, and receive audio alarms when reminder times are reached. All data is stored persistently, so tasks are not lost after restarting the program.

3- Features Add tasks with optional notes List tasks (all, pending, done) Mark tasks as done or pending Delete tasks Set reminders using a specific date and time Set timers using minutes from now Play an MP3 alarm sound when a reminder is triggered Background reminder checking using threading

Persistent storage using JSON files

4- Technologies Used Python 3.13 Object-Oriented Programming (OOP) Dataclasses for data models Threading for background reminder checks Datetime and zoneinfo for time handling Pygame for playing MP3 alarm sounds JSON for persistent storage

5- How to Run the Project 5-1 Clone the repository git clone https://github.com/your-username/task-manager.git cd task-manager 5-2 Create and activate a virtual environment python -m venv .venv .venv\Scripts\activate 5-3 Install dependencies pip install pygame tzdata 5-4 Run the application python Main.py

6- Reminder and Alarm System Reminders are checked in a background thread Alarms can trigger even when the program is waiting for user input When a reminder time is reached: A message is displayed in the terminal An MP3 alarm sound is played Each reminder is triggered only once

7- Project Structure Main.py : Application controller and main loop TaskManager.py: Core business logic IO.py : Command-line input and output Time.py : Time and reminder utilities Storage.py : JSON persistence layer tasks.json : Stored tasks data (auto-generated) alarm.mp3 : Alarm sound file README.md : Project documentation

8- What I Learned Designing modular Python applications Separating concerns between logic, IO, and utilities Working with background threads Handling date and time correctly Persisting application state using JSON Structuring a real-world Python project

9- Future Improvements Graphical user interface Desktop notifications Task priorities Sorting tasks by due date Cross-platform packaging Web or API-based version

10- Author This project was built by Arya as a personal learning project while studying Python and backend development fundamentals.