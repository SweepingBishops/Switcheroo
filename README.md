
# Switcheroo

Switcheroo is a simple Flask-based web server designed to host coding competitions where teams of two people can participate. The server allows users to log in, view questions, submit answers, and track their scores.

## Features

- Teams can log in using credentials specified in the `users.json` file.
- Questions are displayed as images, and answers are validated against the `questions.json` file.
- The server tracks attempts and points, with a maximum of 3(modifiable) attempts per question.

## Requirements

- Python 3.8 or higher
- Flask

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Methaphur/Switcheroo.git
cd Switcheroo
```

### 2. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Flask

Install Flask using pip:

```bash
pip install Flask
```

### 4. Add Questions and Downloadable Resources

You can add questions to the competition by placing image files in the `static/questions` directory. The images should be named in the format `qN.png`, where `N` is the question number.

To include downloadable resources for specific questions, add the `resources` field to the `questions.json` file. Specify the path to the resource file using the format `"\path\to\resource.txt"`.

For example, if you want to include a resource file named `q4_cipher.txt` for question 4, modify the `questions.json` file as follows:

```json
{
    "title": "Question 4",
    "text": "q4.png",
    "answer": "42",
    "resources": "static/questions/q4_cipher.txt"
}
```

Remember to place the resource file in the `static/questions` directory and update the `questions.json` file accordingly for each question that requires a downloadable resource.

### 5. Configure Answers

The correct answers should be specified in the `questions.json` file in the following format:

```json
{
    "title": "Question 3",
    "text": "q3.png",
    "answer": "10061"
}
```

Repeat this format for each question.

### 7. Configure User Logins

User login credentials should be added to the `users.json` file in the following format:

```json
{
    "team_name": "password"
}
```

To ensure secure storage of passwords, you can use the `generate_passwords.py` script provided in the repository. This script hashes the password using SHA-1 and adds it to the `users.json` file.

You can add as many teams as needed.

### 8. Run the Server

To start the Flask server, simply run the `server.py` file:

```bash
python server.py
```

The server will start, and you can access it via your web browser at `http://127.0.0.1:4000/`.