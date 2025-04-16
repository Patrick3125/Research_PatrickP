python acf.py
python save_plot.py

#gnuplot -persist <<-EOFMarker
#plot "../res/res.acf" u 1:2 w l t "CCF(1,1) (ACF of 1)", \
#     '' u 1:2:(\$3*2) every 10 w yerrorbars t "CCF(1,1) Error", \
#     "../res/res.acf" u 1:4 w l t "CCF(2,1)", \
#     '' u 1:4:(\$5*2) every 10 w yerrorbars t "CCF(2,1) Error", \
#     "../res/res.acf" u 1:6 w l t "CCF(1,2)", \
#     '' u 1:6:(\$7*2) every 10 w yerrorbars t "CCF(1,2) Error", \
#     "../res/res.acf" u 1:8 w l t "CCF(2,2) (ACF of 2)", \
#     '' u 1:8:(\$9*2) every 10 w yerrorbars t "CCF(2,2) Error"
##EOFMarker
