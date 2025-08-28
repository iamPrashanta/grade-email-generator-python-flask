# AI-Powered Academic Email Generator

## 📢 What is this project?

A modern web application for schools/colleges that:
- Lets admin/teachers select subjects, enter student grades, and parent info
- Automatically generates a professional, encouraging email about the student’s performance using generative AI (Google Gemini)
- Supports flexible subject selection, organized by academic category, with a searchable modal interface and editable marks.

## 🎬 Demo

> **[Include a GIF or screenshot here showing the admin selecting subjects, entering marks, and getting a ready-to-send email!]**

***

## 🌟 Features

- **Intuitive subject picking**: Search, group, and add from comprehensive subject lists via a modal popup.
- **Editable, user-friendly forms**: Enter grades and update marks on the fly.
- **AI-generated email**: Instantly create a warm, detailed parent notification using Gemini AI.
- **Modern UI/UX**: Responsive, visually harmonized design.
- **Admin-centric workflow**: Save valuable time for teachers and administrators!

***

## 🖥️ How to Use as an End User

1. **Open the web application.**
2. **Click "Select Subjects"** to open the modal, use the search/filter to pick required subjects, and click "Add".
3. **Enter or edit student marks** directly.
4. **Input student and parent information** (names, email).
5. **Submit the form** to generate the AI-based email draft for parents.
6. **Review, accept, re-generate, or send** the email as needed.

***

## 🚀 Installation & Setup (For Developers/Admins)

### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-academic-emailer.git
cd ai-academic-emailer
```

### 2. **Install Dependencies**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 3. **Set Up Environment Variables**

Create a `.env` file with:
```
FLASK_SECRET_KEY=your-secret-key
GOOGLE_API_KEY=your-gemini-api-key
EMAIL_USER=your-email-for-sending@example.com
EMAIL_PASSWORD=your-app-password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
```

### 4. **Run the Application**
```bash
python app.py
```
Open `http://localhost:5000` in your browser.

***

## 🏫 How to Add to Your College/University Website

**For administrators or IT staff:**

1. **Deploy the Flask app** on your institution’s web server or internal network (using WSGI servers like gunicorn, mod_wsgi, etc.).
2. **Integrate with your authentication system** if needed (e.g., SSO or LDAP for teachers/admin access).
3. **Optionally customize subjects/categories** in `static/js/main.js` or wherever the subject data is defined.
4. **Configure mail settings** in `.env` for your institution’s mail system.
5. **Add a link or iframe** to this application from your main college admin portal, or embed as a privileged admin tool.
6. **Test thoroughly on your infrastructure before going live!**

***

## 🛠️ Technologies Used

- Python 3, Flask (web framework)
- Google Gemini Generative AI API
- HTML5, CSS3, JavaScript (modular, static files)
- Responsive, custom modal and table components
- SMTP for email sending

***

## 🤝 Contributing

PRs, issues, and suggestions welcome! Please submit improvements for new subject fields, additional export/email formats, more languages, etc.

***

## 📄 License

MIT or Apache 2.0 (choose one)

***

## 💡 Credits

Inspired by teachers who want to modernize student-parent communication and reduce admin workload.

***

## 🙋 Need Help?

Open an issue on the repo or contact the maintainer at [your.email@example.com].

***

**Want to deploy this at your institution?**  
Just follow the setup above or fork and customize! All core features are modular and the subject list can be adapted according to your curriculum.
