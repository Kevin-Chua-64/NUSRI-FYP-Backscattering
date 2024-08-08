@echo off

rem First, open the GUI, also as a UDP server, always ready to receive packets...
rem Then, loop two files, the first to control Pluto to read data, the second to do FM demod and send a UDP packet after saving the data info.

rem Parallel run
echo Runing GUI...
echo ...
set cmd1=python3 "GUI.py"
start "" /b %cmd1%
timeout /t 1 > nul

rem Loop to run
:loop

echo Receiving data from Pluto...
python "Pluto_runRx.py"

echo Demoding...
python3 "FM_demod_UDP.py"
rem timeout /t 3 /nobreak

goto loop
