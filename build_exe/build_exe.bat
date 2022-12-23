@echo off

if exist build (del /q /s build)
if exist build (rmdir /q /s build)
if exist *.spec (del *.spec)

pyinstaller --noconfirm --onefile --noconsole --icon "my_icon.ico" --name "My_Application" --paths "..\\src\\common" --distpath ".\\" "..\\src\\main.py"
