@echo off
echo Committing changes to utsav branch...
git add main.py
git commit -m "Update main.py: Add initialization log"
git push origin utsav
echo Done!
pause
