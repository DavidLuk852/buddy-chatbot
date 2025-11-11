@echo off
echo Starting Buddy Chatbot...

:: Start client
echo Starting client...
cd C:\Users\lukda\buddy-chatbot\client
start cmd /k npm start

:: Start Python API
echo Starting Python API...
cd C:\Users\lukda\buddy-chatbot\python-api
start cmd /k python app.py

:: Start server
echo Starting server...
cd C:\Users\lukda\buddy-chatbot\server
start cmd /k node server.js

echo All components started.
pause