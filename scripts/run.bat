@echo on

:: Start the server in the background
start /b python src\test_manager\service.py

:: Run the client
python src\test_manager\client.py

:: Kill the server
taskkill /IM python.exe /F
