@ECHO OFF
python "C:\Users\Teemu-amd\Desktop\PYTHON SCRIPTIT\pio-script-builder-v2-git\pio-cl-script-runner\main.py" > Output
SET /p MYVAR=<Output
ECHO %MYVAR%
PAUSE
DEL Output



