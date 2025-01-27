# Impromptle
A web-app that helps user become proficient Public Speakers.

NOTE: You need your own API_Key to run this application as it relies on OpenAI's API

Impromp2 is an innovative web application designed to enhance public speaking skills through real-time practice and feedback. Utilizing advanced artificial intelligence, 
the platform challenges users with randomly selected prompts, encouraging them to articulate their thoughts clearly and confidently within a two-minute timeframe. By 
analyzing eye movements, facial expressions, and audio transcriptions, Impromp2 offers actionable insights to improve engagement and reduce filler words.
In addition to individual practice, Impromp2 will be developed further to foster a supportive community where users can share and review each other’s speeches. By providing 
a space for constructive feedback, users can learn from diverse speaking styles and perspectives. Ultimately, Impromp2 aims to empower individuals to develop effective 
communication skills, preparing them for success in various personal and professional contexts.

Sample Video: Impromptle Sample.mkv

# Setup Process

Follow the steps below to set up and run the project locally.

## Step 1: Activate the Virtual Environment

1. Open a terminal (Command Prompt, PowerShell, or terminal in your IDE).
2. Navigate to the project directory using the `cd` command. For example:
   ```bash
   cd path\to\your\project
   ```
## Step 2: Install Dependencies

If you have a `requirements.txt` file (which is typical), you can install the necessary packages using:
```bash
pip install -r requirements.txt
```

## Step 3: Run Migrations

Before running the server, you usually need to apply any database migrations. In your project directory, run:
```bash
python manage.py migrate
```

## Step 4: Start the Development Server

You can now run the Django development server using:
```bash
python manage.py runserver
```
This will start a local server, and you can typically access your site by going to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.

# Learning Process:
Learning Journey
As an international student, my experience with English Proficiency Tests such as IELTS and TOEFL sparked the inspiration for this project. I realized 
that many students often struggle with fluency and resourcefulness when approaching these assessments. This motivated me to create a platform that not 
only assists in practicing language skills but also empowers users to communicate more effectively in high-pressure situations.

I believe this project has the potential to significantly impact its intended users by providing a supportive and interactive environment for enhancing 
public speaking skills. By leveraging technology, it can help users build confidence and fluency, ultimately benefiting their academic and professional pursuits.

Throughout this journey, I learned to work with Django and various APIs to establish seamless connections between components of the application. I chose 
Django because I had prior experience with Python from several classes, and I saw it as a quick and efficient way to develop a functional project during the hackathon.

However, the process was not without challenges. Collaborating with team members unfamiliar with Git led to merge conflicts that consumed a considerable 
amount of time to resolve. Additionally, integrating the Computer Vision 2 model proved to be a complex task, which is why I opted to use a dummy video for that part of the project. 
