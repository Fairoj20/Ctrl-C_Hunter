# 🔍 UAP CTRL + C Hunter — Smart Plagiarism Detection System

**UAP CTRL + C Hunter** is a full-stack, Django-based plagiarism detection platform developed for the Department of Computer Science & Engineering, **University of Asia Pacific (UAP)**. It enables students, educators, and administrators to verify the originality of academic documents, assignments, and pasted texts using machine learning and natural language processing techniques.

---

## 🌟 Key Features

* **Multi-Format Input Support:** Upload documents (`.pdf`, `.docx`, `.txt`) or directly paste text for instant checking.
* **Intelligent Text Normalization:** Cleans text by lowercasing, stripping punctuation, and filtering out stop-words prior to vectorization.
* **TF-IDF & Cosine Similarity Engine:** Converts documents into numerical vectors and calculates mathematical overlap ranging from 0% to 100%.
* **Color-Coded Similarity Results:** Classifies results with visual status tags (e.g., *Different*, *Somewhat Similar*, *Similar*, *Identical*).
* **Comparison History & Audit Trail:** Automatically archives every comparison with timestamps, source inputs, scores, and status for complete traceability.
* **Text Entry Management (CRUD):** Save, view, update, and delete frequently compared texts and files.
* **Role-Based Profiles:** Distinct interfaces and custom profiles for **Students**, **Teachers**, and **Administrators**.

---

## 🛠️ Technology Stack

* **Backend Framework:** Django (Python)
* **NLP & Machine Learning:** scikit-learn (`TfidfVectorizer`), PyPDF2
* **Frontend:** HTML5, CSS3, Bootstrap
* **Database:** SQLite3 (Development / Testing)
* **Version Control:** Git & GitHub

---

## 📐 How It Works (Algorithmic Pipeline)

1. **Preprocessing & Normalization:** Cleans raw pasted text or extracted document files by lowercasing and removing punctuation/stop-words.
2. **Vector Space Modeling:** Uses Scikit-learn's `TfidfVectorizer` to map words into high-dimensional numerical feature vectors based on term frequency and inverse document frequency.
3. **Cosine Metric Analysis:** Evaluates the cosine of the angle between two multi-dimensional document vectors to produce an accurate overlap score:
   $$\text{Similarity}(A, B) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$$
4. **Classification & Feedback:** Maps similarity percentage into actionable color-coded status badges for quick visual assessment.

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
---

## 🚀 Installation & Local Setup
Prerequisites
Python 3.10+

Git

pip package manager

Steps
1.Clone the Repository:
git clone [https://github.com/anjumaAlam/Ctrl-C_Hunter.git](https://github.com/anjumaAlam/Ctrl-C_Hunter.git)
cd Ctrl-C_Hunter

2.Create and Activate Virtual Environment:

# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate

3.Install Dependencies:

pip install -r requirements.txt

4.Start the Development Server:

python manage.py runserver

Open your browser and visit: http://127.0.0.1:8000/
---
## 👥 Contributors (Team CTRL + C Hunter)
Fairoj Salim :

Top Contributor: 9 Commits | 663 Lines Added | 31 Lines Deleted

Lead contributions across user interface, profile management, and document comparison workflows.

Anjuma Alam :

7 Commits | Core repository setup, architecture implementation, and ML similarity pipelines.

Suzana Sehreen :

5 Commits | Functional testing, template structuring, and documentation support.
---
## 🎓 Academic Information
Developed as part of Course CSE 302: Object-Oriented Programming II and Web Programming Lab, Department of Computer Science & Engineering, University of Asia Pacific (UAP).
