## Installation Guide
You need node@latest and python@3.9-3.11 (any version that supports tensorflow)
### Steps
1. clone the repository ``git clone git@github.com:wayleem/professor-chatbot.git``
2. cd into it run ``npm i`` in **client/**
3. cd to **ai/** and run ``pip install numpy nltk tensorflow flask flask-cors``
   a. you may need to install ``venv`` virtual environment. ``python3 -m venv .``
   b. run ``source bin/activate``, and then you can run the pip install commands fom 3.
   c. run ``python3`` and enter ``import nltk`` and ``nltk.download('punkt')``.
5. run ``python3 training.py`` in **ai/** to generate a chatbot model.
6. run ``python3 chatbot_api.py`` in **ai/** to start the api server.
7. cd into **client/** and run ``npm run dev``
8. you should be able to test out the application in the localhost port of your **client/**

### note
the localhost intended to be port 5173.
