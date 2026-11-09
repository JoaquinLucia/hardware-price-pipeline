from app.servicios.observador import gestor_logs_global, ObservadorConsola, ObservadorSocket

# Le decimos al gestor que queremos ver los logs en consola y mandarlos al servidor
gestor_logs_global.adjuntar(ObservadorConsola())
gestor_logs_global.adjuntar(ObservadorSocket())

# A partir de acá, cualquier scraper que use @registro_log_scraper 
# mandará el mensaje a ambos destinos simultáneamente.