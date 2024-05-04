set datafile separator ","
set terminal png
set output "comparison_one.png"
set title "Comparison of Load Test Results"
set xlabel "Requests"
set ylabel "Requests per second"
set key left top
set style data lines

set multiplot layout 3, 1 title "Load Test Results"

# Registro
set title "Registro"
plot "load_test_results_registro_v2.csv" every ::1 using 1:3 title "Nube"

# Inicio de sesión
set title "Inicio de sesión"
plot "load_test_results_inicio_de_sesion_v2.csv" every ::1 using 1:3 title "Nube"

# Carga de video
set title "Carga de video"
plot "load_test_results_carga_de_video_v2.csv" every ::1 using 1:3 title "Nube"

unset multiplot