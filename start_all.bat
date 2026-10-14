@echo off
start "Product API - 5000" cmd /k "cd /d D:\IBM_Project\product_api && python app.py"
start "Dealer API - 8080" cmd /k "cd /d D:\IBM_Project\dealer_api && npm start"
start "Frontend - 5001" cmd /k "cd /d D:\IBM_Project\frontend && python app.py"
echo.
echo All three servers are starting.
echo Wait until the three terminal windows show that they are running.
echo Then open http://127.0.0.1:5001
pause
