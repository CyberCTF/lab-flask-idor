# Flask IDOR: Insecure Direct Object Reference Lab

## Description
Learn how a lack of authorization checks in a Flask application's download endpoint can allow attackers to access or exfiltrate other users' files.

## Default Credentials
- Username: `alice`
- Password: `alicepass`

## Objectives
- Identify endpoints vulnerable to IDOR
- Craft and send unauthorized resource access requests
- Verify access to data owned by other users

## Difficulty
Beginner

## Estimated Time
30 minutes

## Prerequisites
- Basic Flask knowledge
- HTTP fundamentals
- Familiarity with browser developer tools or curl

## Skills Learned
- Finding and exploiting IDOR in Flask routes
- Testing for insufficient access control
- Validating and reporting sensitive data exposure

## Project Structure
- folder: build
- folder: deploy
- folder: test
- folder: docs
- file: README.md
- file: .gitignore

## Quick Start
**Prerequisites:** Docker or Python 3 with virtualenv installed.

**Installation:**
```sh
git clone <repo-url>
cd flask-idor-lab
docker-compose up
# or:
pip install -r build/requirements.txt
cd build
flask run
```

## Issue Tracker
https://github.com/example/flask-idor-lab/issues 