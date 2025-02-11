python acf.py

gnuplot -persist <<-EOFMarker
plot "../res/res.acf" u 1:2 w l t "sim res",'' u 1:2:(\$3*2) every 10 w ye t ""
EOFMarker
