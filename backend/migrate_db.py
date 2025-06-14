#!/usr/bin/env python3
"""
Script de migración para agregar el campo duration a la tabla playlist_media
"""
import sqlite3
import os
import sys

def migrate_database():
    """Migrar la base de datos para agregar el campo duration a playlist_media"""
    db_path = "signance.db"
    
    if not os.path.exists(db_path):
        print(f"Error: Base de datos {db_path} no encontrada")
        sys.exit(1)
    
    # Hacer backup de la base de datos
    backup_path = f"{db_path}.backup"
    if not os.path.exists(backup_path):
        print(f"Creando backup en {backup_path}...")
        import shutil
        shutil.copy2(db_path, backup_path)
        print("Backup creado exitosamente")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar si la columna duration ya existe
        cursor.execute("PRAGMA table_info(playlist_media);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'duration' in column_names:
            print("La columna 'duration' ya existe en la tabla playlist_media")
            return
        
        print("Agregando columna 'duration' a la tabla playlist_media...")
        
        # Agregar la nueva columna
        cursor.execute("""
            ALTER TABLE playlist_media 
            ADD COLUMN duration INTEGER;
        """)
        
        conn.commit()
        print("Migración completada exitosamente")
        
        # Verificar la nueva estructura
        cursor.execute("PRAGMA table_info(playlist_media);")
        columns = cursor.fetchall()
        print("\nNueva estructura de la tabla playlist_media:")
        for column in columns:
            nullable = "NO" if column[3] == 1 else "YES"
            default = f" DEFAULT {column[4]}" if column[4] is not None else ""
            print(f"- {column[1]} {column[2]} (NULL: {nullable}){default}")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
