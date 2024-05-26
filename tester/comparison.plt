set datafile separator ","
set terminal png
set output "comparison_time_per_request.png"
set title "Comparison of Load Test Results"
set xlabel "Requests"
set ylabel "Requests per second"
set key left top

set style data lines

set multiplot layout 3, 1 title "Load Test Results"

set title "Registro"
plot "load_test_results_registro_v2.csv" every ::1 using 1:4 title "Version 2", \
     "load_test_results_registro_v1.csv" every ::1 using 1:4 title "Version 1"

set title "Inicio de sesión"
plot "load_test_results_inicio_de_sesion_v2.csv" every ::1 using 1:4 title "Version 2", \
     "load_test_results_inicio_de_sesion_v1.csv" every ::1 using 1:4 title "Version 1"

set title "Carga de video"
plot "load_test_results_carga_de_video_v2.csv" every ::1 using 1:4 title "Version 2", \
     "load_test_results_carga_de_video_v1.csv" every ::1 using 1:4 title "Version 1"

unset multiplot