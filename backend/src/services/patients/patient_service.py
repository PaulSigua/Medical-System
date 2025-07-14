from database.db import get_db_connection
from fastapi import HTTPException
import os
import shutil

def delete_patient_by_id(patient_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print(f"Eliminando paciente con el idL {patient_id}")
        
        # Eliminar en orden de dependencias
        cursor.execute("DELETE FROM diagnostics WHERE patient_id = %s", (patient_id,))
        cursor.execute("DELETE FROM predictions WHERE patient_id = %s", (patient_id,))
        cursor.execute("DELETE FROM surveys WHERE patient_id = %s", (patient_id,))
        cursor.execute("DELETE FROM reports WHERE patient_id = %s", (patient_id,))
        cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        delete_patients_files(patient_id)
        
        print(f"Paciente {patient_id} eliminado correctamente.")
        
        return True
    
    except Exception as e:
        print(f"Error al eliminar paciente: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar paciente")
    
def delete_patients_files(patient_id: str):
    try:
        uploads_dir = "src/uploads"
        static_dir = "src/static"
        
        # Eliminar todas las carpetas que contienen el patient_id
        for base_dir in [uploads_dir, static_dir]:
            for folder_name in os.listdir(base_dir):
                if patient_id in folder_name:
                    path_to_delete = os.path.join(base_dir, folder_name)
                    print(f"Eliminando carpeta: {path_to_delete}")
                    shutil.rmtree(path_to_delete, ignore_errors=True)

    except Exception as e:
        print(f"Error al eliminar archivos del paciente {patient_id}: {e}")