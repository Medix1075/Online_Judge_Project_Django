# 🧠 AI-Powered Online Judge

A scalable, full-stack online judge platform designed for real-time evaluation of user-submitted code, enhanced with AI-powered feedback and robust deployment.

🌐 [Live Demo](http://13.60.72.253/home/) | 🎥 [Video Walkthrough](https://www.loom.com/share/6286f60e130a4b87a61643fcb18bebc0?sid=9a051ceb-e91d-42e1-ad30-c880720333a6)

---

## 🚀 Overview

Built a scalable online judge using **Django** and **Docker**, enabling secure execution of user-submitted code with ~300ms median latency under 1,200+ concurrent submissions. Metadata is stored in **SQLite** for lightweight, low-latency access.

Integrated **Google Gemini API** for real-time AST-level code analysis and semantic embedding comparison, enabling token-wise feedback generation with a decent match accuracy in conceptual hinting benchmarks.

The system is deployed on **AWS EC2** with a production-grade frontend using **Tailwind CSS**, resulting in a secure and responsive user experience. Developed under mentorship from engineers at **Google, Apple, ByteDance**, and **Alphagrep Singapore**.

---

## ⚙️ Tech Stack

- **Backend:** Django, Docker, SQLite
- **Frontend:** Tailwind CSS, HTMX
- **AI Integration:** Google Gemini API (AST + embeddings)
- **Deployment:** AWS EC2 (Ubuntu)
- **Containerization:** Docker (secure code sandboxing)

---

## 🔑 Features

- 👤 User Authentication & Submission History
- 🧠 AI-Powered Code Review (via Gemini)
- ⚙️ Real-Time Code Execution in Isolated Docker Containers
- 📊 Scalable Execution Engine (Handles 1200+ concurrent runs)
- 🌐 Lightweight Web Interface with Tailwind CSS
- 📁 Admin Panel for Problem Management
- 📄 Code Hinting with AST & Semantic Match
