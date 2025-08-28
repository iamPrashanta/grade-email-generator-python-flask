import os
import google.generativeai as genai
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'ASDFGHJKLERTYUIO4567809876545678')

# Configure Google Generative AI with your API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create model instance for Gemini 1.5 Flash
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_grades(grade_input):
    """Parse flexible grade input into a dictionary"""
    grades = {}
    for part in grade_input.split(','):
        if ':' in part:
            subject, score = part.split(':', 1)
            grades[subject.strip()] = score.strip()
    return grades

def generate_email_content(student_name, parent_name, grades_dict):
    grades_str = ", ".join(f"{subj}: {score}" for subj, score in grades_dict.items())
    prompt = (
        f"Write a warm, professional email to {parent_name} about their child {student_name}'s academic performance.\n"
        f"Grades: {grades_str}\n"
        f"If this child got Grades zero in any subject then write 'tumse na ho paiga'."
    )

    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error generating email: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_email', methods=['POST'])
def generate_email():
    student_name = request.form.get('student_name', '').strip()
    parent_name = request.form.get('parent_name', '').strip()
    parent_email = request.form.get('parent_email', '').strip()
    grades_input = request.form.get('grades', '').strip()

    if not (student_name and parent_name and parent_email and grades_input):
        flash("All fields are required.")
        return redirect(url_for('index'))

    grades_dict = parse_grades(grades_input)
    if not grades_dict:
        flash('Please enter grades in the format: "Subject:Score", separated by commas.')
        return redirect(url_for('index'))

    email_content = generate_email_content(student_name, parent_name, grades_dict)

    session['email_data'] = {
        'student_name': student_name,
        'parent_name': parent_name,
        'parent_email': parent_email,
        'grades': grades_dict,
        'email_content': email_content,
    }

    return render_template('review_email.html', data=session['email_data'])

@app.route('/regenerate_email', methods=['POST'])
def regenerate_email():
    if 'email_data' not in session:
        flash("Session expired. Please start again.")
        return redirect(url_for('index'))

    data = session['email_data']
    new_content = generate_email_content(
        data['student_name'],
        data['parent_name'],
        data['grades']
    )
    data['email_content'] = new_content
    session['email_data'] = data

    return render_template('review_email.html', data=data)

@app.route('/send_email', methods=['POST'])
def send_final_email():
    data = session.pop('email_data', None)
    if not data:
        flash("Session expired. Please start again.")
        return redirect(url_for('index'))

    # TODO: Add SMTP email sending logic here

    flash(f"✅ Email generated successfully for {data['student_name']}! (Sending not implemented)")
    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
