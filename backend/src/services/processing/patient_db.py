from database.db import get_db_connection

def get_patient_paths(patient_id: str, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t1ce_path, t2_path, flair_path, t1_path 
        FROM patients 
        WHERE patient_id = %s AND user_id = %s
    """, (patient_id, user_id))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def update_patient_paths(patient_id, user_id, t1ce, t2, flair, t1):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients 
        SET t1ce_path = %s, t2_path = %s, flair_path = %s, t1_path = %s
        WHERE patient_id = %s AND user_id = %s
    """, (t1ce, t2, flair, t1, patient_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()
