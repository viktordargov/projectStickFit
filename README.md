
# Project StickFit - Django Project Definition 🚀

A fitness application with the main goal for providing an easy-to-use interface for custom workouts setup by a trainer. 
Additional features include a forum and image sharing, but are considered secondary features.

---

## 📥 1. Clone the Repository

```bash
git clone https://github.com/viktordargov/projectStickFit.git
cd your-repository
```

---

## 💻 2. Create a Virtual Environment

1. Create the virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate it:

   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

---

## 📦 3. Install Dependencies

Install all the required packages:

```bash
pip install -r requirements.txt
```

---

## 🛠️ 4. Set Up the PostgreSQL Database

1. Install PostgreSQL from [here](https://www.postgresql.org/download/).
2. Open your PostgreSQL CLI or a database management tool.
3. Create a new database:
   ```sql
   CREATE DATABASE your_database_name;
   ```
4. Update the `DATABASES` section in your `settings.py` file with your PostgreSQL credentials.
         

---

## 🔄 5. Apply Migrations

Run the following command to create the necessary database tables:

```bash
python manage.py migrate
```

---

## 📋 6. Load Data into the Database

1. Run the following commands **in order** to populate the database:

   ```bash
   python manage.py shell < path_to_populate_exercises.py
   python manage.py shell < path_to_populate_workouts.py
   ```

2. Replace `path_to_populate_exercises.py` and `path_to_populate_workouts.py` with the actual file paths.

---

## ▶️ 7. Start the Development Server

Run the server:

```bash
python manage.py runserver
```

---

## 📝 Notes for SoftUni

- Currently project is setup with decouple to hide the sensitive details, this includes PostgreSQL credentials.
- Cloudinary setup details were shared in the project submission form.
- While available in the project, details for Mailjet / Redis Cloud were not shared via the above form as they were not ready. As such password reset will not function with the current settings.

