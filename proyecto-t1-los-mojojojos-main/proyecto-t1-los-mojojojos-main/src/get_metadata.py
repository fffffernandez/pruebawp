"""
Script para obtener el rango de fechas y otros metadatos de la base de datos
"""
from database import execute_query

def get_metadata():
    # Obtener rango de meses y días
    query = """
        SELECT 
            MIN(month) as min_month, 
            MAX(month) as max_month,
            MIN(day_of_month) as min_day,
            MAX(day_of_month) as max_day,
            MIN(hour) as min_hour,
            MAX(hour) as max_hour
        FROM consumo_modelo;
    """
    result = execute_query(query, fetch_one=True)
    
    print("="*60)
    print("METADATOS DE LA BASE DE DATOS")
    print("="*60)
    print(f"Rango de Meses: {result['min_month']} - {result['max_month']}")
    print(f"Rango de Días del mes: {result['min_day']} - {result['max_day']}")
    print(f"Rango de Horas: {result['min_hour']} - {result['max_hour']}")
    print()
    
    # Obtener lista de zonas
    zonas = [
        'albaicin_alto', 'albaicin_bajo', 'bola_de_oro', 'camino_ronda',
        'cartuja', 'centro_catedral', 'cervantes', 'chana_barrio',
        'chana_bobadilla', 'fuentenueva', 'mercagranada', 'norte_almanjayar',
        'pedro_antonio', 'periodistas', 'plaza_toros', 'pts_tecnologico',
        'realejo', 'sacromonte', 'zaidin_nuevo', 'zaidin_vergeles'
    ]
    
    print(f"Total de Zonas: {len(zonas)}")
    print("Zonas disponibles:")
    for i, zona in enumerate(zonas, 1):
        print(f"  {i}. {zona.replace('_', ' ').title()}")

if __name__ == "__main__":
    get_metadata()
