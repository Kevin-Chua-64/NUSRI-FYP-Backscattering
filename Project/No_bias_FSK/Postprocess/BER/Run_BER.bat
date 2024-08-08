@echo off

rem First, collect data from Pluto
rem Then, do FM demod calculate BER

:loop

echo Receiving data from Pluto...
python "Pluto_runRx_BER.py"

echo Demoding...
python3 "FM_demod_BER.py"
pause

goto loop
