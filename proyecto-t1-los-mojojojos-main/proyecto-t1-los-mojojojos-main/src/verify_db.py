"""
Script para verificar la estructura de la base de datos
"""
from database import test_connection, get_table_names, get_table_columns, execute_query

def main():
    print("=" * 80)
    print("VERIFICACIÓN DE LA BASE DE DATOS")
    print("=" * 80)
    print()
    
    # Probar conexión
    print("1. Probando conexión...")
    if not test_connection():
        print("No se pudo conectar a la base de datos. Verifica las credenciales.")
        return
    
    print()
    print("2. Obteniendo lista de tablas...")
    tables = get_table_names()
    
    if not tables:
        print("   No se encontraron tablas en la base de datos.")
        return
    
    print(f"   ✓ Se encontraron {len(tables)} tabla(s)")
    print()
    
    # Mostrar información de cada tabla
    print("3. Estructura de las tablas:")
    print("-" * 80)
    
    for table in tables:
        print(f"\n📊 Tabla: {table}")
        print("   Columnas:")
        
        columns = get_table_columns(table)
        for col in columns:
            print(f"      - {col['column_name']} ({col['data_type']})")
        
        # Contar registros
        try:
            count_query = f"SELECT COUNT(*) as total FROM {table};"
            result = execute_query(count_query, fetch_one=True)
            print(f"   📈 Total de registros: {result['total']}")
            
            # Mostrar muestra de datos (primeras 3 filas)
            if result['total'] > 0:
                sample_query = f"SELECT * FROM {table} LIMIT 3;"
                samples = execute_query(sample_query)
                print("   📝 Muestra de datos (primeras 3 filas):")
                for i, row in enumerate(samples, 1):
                    print(f"      Fila {i}: {dict(row)}")
        except Exception as e:
            print(f"   ⚠ Error obteniendo datos: {e}")
        
        print("-" * 80)

if __name__ == "__main__":
    main()
