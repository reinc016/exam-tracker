# Exam Readiness Tracker

A high-performance academic management dashboard designed to solve the complexity of tracking multi-subject exam preparation. Built with a relational architecture to ensure data integrity and real-time progress visualization.

## 💡 Why This Project?
Most study trackers rely on flat files or simple lists that lose integrity as projects grow. I engineered this tool using **SQLAlchemy** to implement a **Relational Data Model**, enabling:
* **One-to-Many Relationships:** Automatically link multiple study modules to specific subjects.
* **Data Consistency:** Ensure that completion metrics are always synchronized with the underlying database state[cite: 1].
* **Scalability:** A modular design that allows for adding new features without refactoring core logic[cite: 1].

## 🛠 Engineering Stack
* **Frontend & Logic:** Streamlit (for high-speed, interactive dashboards)[cite: 1].
* **Backend & ORM:** Python + SQLAlchemy (for robust, object-oriented database management)[cite: 1].
* **Persistence:** SQLite (optimized for efficient, lightweight data storage)[cite: 1].

## 🚀 Key Technical Implementations
* **CRUD Operations:** Implemented full Create, Read, Update, and Delete workflows to manage academic progress end-to-end[cite: 1].
* **State Management:** Utilized Streamlit’s session state to provide a seamless user experience during data manipulation[cite: 1].
* **Modular Architecture:** Structured the codebase into `models.py` (data schema), `database.py` (persistence layer), and `app.py` (UI/UX) to follow professional development standards[cite: 1].

## 📋 How to Deploy
1. **Clone the repository:** `git clone <exam-tracker-url>`
2. **Install requirements:** `pip install -r requirements.txt`
3. **Execute:** `streamlit run app.py`
