# 🔍 UAP CTRL + C Hunter — Smart Plagiarism Detection System

**UAP CTRL + C Hunter** is a full-stack, Django-based plagiarism detection platform developed for the Department of Computer Science & Engineering, **University of Asia Pacific (UAP)**. It enables students, educators, and administrators to verify the originality of academic documents, assignments, and pasted texts using machine learning and natural language processing techniques[cite: 29, 34].

---

## 🌟 Key Features

* **Multi-Format Input Support:** Upload documents (`.pdf`, `.docx`, `.txt`) or directly paste text for instant checking[cite: 33].
* **Intelligent Text Normalization:** Cleans text by lowercasing, stripping punctuation, and filtering out stop-words prior to vectorization[cite: 34].
* **TF-IDF & Cosine Similarity Engine:** Converts documents into numerical vectors and calculates mathematical overlap ranging from 0% to 100%[cite: 34].
* **Color-Coded Similarity Results:** Classifies results with visual status tags (e.g., *Different*, *Somewhat Similar*, *Similar*, *Identical*)[cite: 34, 47].
* **Comparison History & Audit Trail:** Automatically archives every comparison with timestamps, source inputs, scores, and status for complete traceability[cite: 30, 34, 47].
* **Text Entry Management (CRUD):** Save, view, update, and delete frequently compared texts and files[cite: 33].
* **Role-Based Profiles:** Distinct interfaces and custom profiles for **Students**, **Teachers**, and **Administrators**[cite: 30, 34].

---

## 🛠️ Technology Stack

* **Backend Framework:** Django (Python)[cite: 32, 33]
* **NLP & Machine Learning:** scikit-learn (`TfidfVectorizer`), PyPDF2[cite: 34, 35]
* **Frontend:** HTML5, CSS3, Bootstrap[cite: 36]
* **Database:** SQLite3 (Development / Testing)[cite: 33, 36]
* **Version Control:** Git & GitHub[cite: 40, 41]

---

## 📁 Project Structure

```text
Ctrl-C_Hunter/
├── accounts/                  # User registration, profiles, and role management
│   ├── templates/accounts/    # Dashboard, Login, Register, Profile templates
│   ├── models.py              # UserProfile model (role, institution, bio, phone)
│   ├── views.py
│   └── urls.py
├── checker/                   # Plagiarism engine and document management
│   ├── templates/checker/     # Comparison, History, and Entry CRUD templates
│   ├── models.py              # TextEntry and ComparisonHistory models
│   ├── utils.py               # Text normalization and vector similarity logic
│   ├── views.py
│   └── urls.py
├── plagiarism_checker/        # Core Django settings, URLs, and WSGI/ASGI
├── manage.py
├── requirements.txt
└── db.sqlite3

```

---

## 🚀 Setup and Installation

Follow these steps to run Ctrl-C Hunter on your local machine.

### Prerequisites
- Python 3.10+ installed
- Git installed
- `pip` package manager

### 1. Clone the Repository
```bash
git clone https://github.com/anjumaAlam/Ctrl-C_Hunter.git
cd Ctrl-C_Hunter
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser!

---

## 👥 Contributors (Team CTRL + C Hunter)
Fairoj Salim :

Top Contributor: 9 Commits | 663 Lines Added | 31 Lines Deleted

Lead contributions across user interface, profile management, and document comparison workflows.

Anjuma Alam (23101164) :

7 Commits | Core repository setup, architecture implementation, and ML similarity pipelines.

Suzana Sehreen (23101139) :

5 Commits | Functional testing, template structuring, and documentation support.

## 🎓 Academic Information
Developed as part of Course CSE 302: Object-Oriented Programming II and Web Programming Lab, Department of Computer Science & Engineering, University of Asia Pacific (UAP).
