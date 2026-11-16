import web
from mvc.models.conexion import obtener_conexion
from laboratorio import logger

# Renderizamos index.html de forma independiente porque ya incluye su propio Navbar y Footer
render = web.template.render('mvc/views/')


class Index:
    def GET(self):
        ranking = self._obtener_top_marcador()
        return render.index(ranking)

    def _obtener_top_marcador(self):
        """Consulta el Top 5 de XP en PostgreSQL; usa datos demo si aún no hay registros."""
        conn = obtener_conexion()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            u.nombre AS nombre,
                            u.usuario AS matricula,
                            COALESCE(g.nombre, 'Meca 3°A') AS grupo,
                            COUNT(DISTINCT i.asignacion_id) AS completadas,
                            COALESCE(SUM(mejores.max_xp), 0) AS mejor_xp
                        FROM usuarios u
                        LEFT JOIN grupo_alumno ga ON u.id = ga.alumno_id
                        LEFT JOIN grupos g ON ga.grupo_id = g.id
                        LEFT JOIN (
                            SELECT alumno_id, asignacion_id, MAX(xp_obtenida) AS max_xp
                            FROM intentos
                            GROUP BY alumno_id, asignacion_id
                        ) mejores ON u.id = mejores.alumno_id
                        LEFT JOIN intentos i ON u.id = i.alumno_id
                        WHERE u.rol = 'Alumno' AND u.activo = TRUE
                        GROUP BY u.id, u.nombre, u.usuario, g.nombre
                        ORDER BY mejor_xp DESC
                        LIMIT 5;
                    """)
                    filas = cur.fetchall()
                    if filas and len(filas) > 0:
                        return filas
            except Exception as e:
                logger.warning(f"No se pudo cargar ranking real en index (usando vista previa): {e}")
            finally:
                conn.close()

        # Datos de respaldo para que el marcador siempre luzca como en el diseño
        return [
            {"nombre": "Valeria Téllez", "matricula": "2023-MEC-0142", "grupo": "Meca 3°A", "completadas": 3, "mejor_xp": 2780},
            {"nombre": "Mateo Reyes", "matricula": "2023-MEC-0089", "grupo": "Meca 3°A", "completadas": 3, "mejor_xp": 2410},
            {"nombre": "Emiliano Mora", "matricula": "2023-MEC-0211", "grupo": "Meca 3°A", "completadas": 3, "mejor_xp": 2295},
            {"nombre": "Sofía Hernández", "matricula": "2023-MEC-0305", "grupo": "Meca 3°A", "completadas": 2, "mejor_xp": 2150},
            {"nombre": "Diego González", "matricula": "2023-MEC-0044", "grupo": "Meca 3°A", "completadas": 2, "mejor_xp": 2020},
        ]