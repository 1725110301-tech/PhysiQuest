import web
from laboratorio import logger

# Definición de rutas MVC en web.py
urls = (
    '/', 'mvc.controllers.index.Index',
    '/login', 'mvc.controllers.login.Login',
    '/logout', 'mvc.controllers.logout.Logout',
    '/dashboard', 'mvc.controllers.dashboard.Dashboard',
    '/practicas', 'mvc.controllers.practicas.Practicas',
    '/simulacion/(.+)', 'mvc.controllers.simulacion.Simulacion',
    '/leaderboard', 'mvc.controllers.leaderboard.Leaderboard',
)

app = web.application(urls, globals())

# Configuración de sesiones
web.config.session_parameters['cookie_name'] = 'utec_physiquest_session'
web.config.session_parameters['timeout'] = 3600

if __name__ == "__main__":
    logger.info("Iniciando servidor PhysiQuest (UTEC) en http://localhost:8080 ...")
    app.run()