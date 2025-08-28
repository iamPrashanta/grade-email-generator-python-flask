import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'NEWSECRET')

# Configure Google Generative AI
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in environment variables.")

genai.configure(api_key=API_KEY)

# Create Gemini model instance
model = genai.GenerativeModel('gemini-1.5-flash')

# SMTP Config (Optional)
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT', 587)
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')


# ---------------------------
# Utility Functions
# ---------------------------

def parse_grades(grade_input: str) -> dict:
    """Convert 'Subject:Score' input into dictionary."""
    grades = {}
    for part in grade_input.split(','):
        if ':' in part:
            subject, score = part.split(':', 1)
            grades[subject.strip()] = score.strip()
    return grades


def generate_email_content(student_name: str, parent_name: str, grades_dict: dict) -> str:
    """Generate personalized email content using Gemini model."""
    grades_str = ", ".join(f"{subj}: {score}" for subj, score in grades_dict.items())
    prompt = (
        f"Write a warm, professional email to {parent_name} about their child {student_name}'s academic performance.\n"
        f"Grades: {grades_str}\n"
        f"Congratulate on good performance and encourage further improvement.\n"
        f"Keep the tone positive, respectful, and concise."
    )

    try:
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, 'text') else "Failed to generate email content."
    except Exception as e:
        return f"Error generating email: {e}"


def send_email(to_email: str, subject: str, body: str):
    """Send email using SMTP (optional feature)."""
    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASS]):
        raise ValueError("SMTP settings are not configured.")

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())


# ---------------------------
# Routes
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_email', methods=['POST'])
def generate_email():
    student_name = request.form.get('student_name', '').strip()
    parent_name = request.form.get('parent_name', '').strip()
    parent_email = request.form.get('parent_email', '').strip()
    grades_input = request.form.get('grades', '').strip()

    # Validate input
    if not (student_name and parent_name and parent_email and grades_input):
        flash("All fields are required.")
        return redirect(url_for('index'))

    grades_dict = parse_grades(grades_input)
    if not grades_dict:
        flash('Invalid format! Use: "Subject:Score", separated by commas.')
        return redirect(url_for('index'))

    email_content = generate_email_content(student_name, parent_name, grades_dict)

    session['email_data'] = {
        'student_name': student_name,
        'parent_name': parent_name,
        'parent_email': parent_email,
        'grades': grades_dict,
        'email_content': email_content
    }

    return render_template('review_email.html', data=session['email_data'])


@app.route('/regenerate_email', methods=['POST'])
def regenerate_email():
    if 'email_data' not in session:
        flash("Session expired. Please start again.")
        return redirect(url_for('index'))

    data = session['email_data']
    new_content = generate_email_content(data['student_name'], data['parent_name'], data['grades'])
    data['email_content'] = new_content
    session['email_data'] = data

    return render_template('review_email.html', data=data)


@app.route('/send_email', methods=['POST'])
def send_final_email():
    data = session.pop('email_data', None)
    if not data:
        flash("Session expired. Please start again.")
        return redirect(url_for('index'))

    try:
        # Uncomment if SMTP is configured:
        # send_email(data['parent_email'], f"Performance Update for {data['student_name']}", data['email_content'])
        flash(f"✅ Email generated successfully for {data['student_name']}! (Sending logic placeholder)")
    except Exception as e:
        flash(f"Error sending email: {e}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
