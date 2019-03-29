move *.log C:\gnuplot\bin\
del C:\gnuplot\bin\lastplot.plt
move lastplot.plt C:\gnuplot\bin\
cd C:\gnuplot\bin\
gnuplot.exe lastplot.plt
pause