gnuplot -persist <<-EOFMarker
plot "../res/surcov1.txt" u 1:2 w l t "A",'' u 1:3 w l t "B"
EOFMarker
