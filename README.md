## Installation Guide
You need node@latest and python@3.9.11
### Steps
1. clone the repository ``git clone git@github.com:wayleem/professor-chatbot.git``
2. cd into it run ``npm i`` in **client/**
3. cd to **ai/** and run ``pip install numpy nltk tensorflow``
4. run ``python training.py`` in **ai/** to generate a chatbot model.
5. run ``python chatbot_api.py`` in **ai/** to start the api server.
6. cd into **client/** and run ``npm run dev``
7. you should be able to test out the application in the localhost port of your **client/**
