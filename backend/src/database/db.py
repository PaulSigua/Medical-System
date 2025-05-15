import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Obtener la ruta del archivo .env
env_path = os.path.join(os.path.dirname(__file__), '..', 'services', '.env')
load_dotenv(dotenv_path=os.path.abspath(env_path))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Crear la URL de conexión correctamente
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para obtener conexión usando psycopg2
def get_db_connection():
    print("Connecting to the database...")
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Función para inicializar las tablas
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Crear tablas principales
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255),
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        agree_terms BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        patient_id VARCHAR(255) NOT NULL,
        patient_name VARCHAR(255) NOT NULL,
        patient_age INT NOT NULL,
        patient_gender VARCHAR(10) NOT NULL,
        prediagnosis TEXT NOT NULL,
        video BYTEA NOT NULL,
        AI_BraTs_Function_report BYTEA NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        patient_id VARCHAR(255) NOT NULL UNIQUE,
        numero_historia_clinica VARCHAR(255) NOT NULL,
        survey_completed BOOLEAN DEFAULT FALSE,
        t1ce_path TEXT,
        t2_path TEXT,
        flair_path TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        token VARCHAR(255) NOT NULL,
        expiration TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS diagnostics (
        id SERIAL PRIMARY KEY,
        patient_id VARCHAR(255) NOT NULL,
        user_id INT NOT NULL,
        description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS reports (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        patient_id VARCHAR(255) NOT NULL,
        report_text2 TEXT NOT NULL,
        report_text5 TEXT NOT NULL,
        graph2_image_path TEXT NOT NULL,
        graph5_image_path TEXT NOT NULL,
        feedback JSON NOT NULL,
        modalities_description TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS surveys (
        id SERIAL PRIMARY KEY,
        patient_id VARCHAR(255) NOT NULL,
        ayudo_ia VARCHAR(50) NOT NULL,
        mejoro_ia BOOLEAN NOT NULL,
        comentarios_adicionales TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
        CONSTRAINT unique_patient_id UNIQUE (patient_id)
    );
    """)

    conn.commit()

    # Cambios adicionales a diagnostics
    cursor.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'cancer_status') THEN
            CREATE TYPE cancer_status AS ENUM ('no se detecta cancer', 'cancer detectado', 'diagnostico incierto');
        END IF;

        IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'has_cancer') THEN
            ALTER TABLE diagnostics DROP COLUMN has_cancer;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'is_generated') THEN
            ALTER TABLE diagnostics ADD COLUMN is_generated BOOLEAN DEFAULT FALSE;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'cancer_status') THEN
            ALTER TABLE diagnostics ADD COLUMN cancer_status cancer_status DEFAULT 'diagnostico incierto';
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'cancer_prediction') THEN
            ALTER TABLE diagnostics ADD COLUMN cancer_prediction BOOLEAN;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'is_generated_by_ia') THEN
            ALTER TABLE diagnostics ADD COLUMN is_generated_by_ia BOOLEAN DEFAULT FALSE;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'report_path') THEN
            ALTER TABLE diagnostics ADD COLUMN report_path TEXT;
        END IF;

        IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'diagnostics' AND column_name = 'updated_at') THEN
            ALTER TABLE diagnostics ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        END IF;
    END
    $$;
    """)
    conn.commit()

    # Trigger para actualizar updated_at
    cursor.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger WHERE tgname = 'set_updated_at'
        ) THEN
            CREATE TRIGGER set_updated_at
            BEFORE UPDATE ON diagnostics
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        END IF;
    END;
    $$;
    """)
    conn.commit()

    # Columnas adicionales en patients
    cursor.execute("""
        DO $$
        DECLARE
            cols TEXT[] := ARRAY[
                'graph1_path', 'graph2_path', 'graph3_path', 'graph4_path',
                'graph5_path', 'graph6_path', 'graph_segmentation_path', 't1_path'
            ];
            col TEXT;
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'patients' AND column_name = 'predicted_segmentation'
            ) THEN
                ALTER TABLE patients ADD COLUMN predicted_segmentation JSONB;
            END IF;

            FOREACH col IN ARRAY cols
            LOOP
                EXECUTE format(
                    'ALTER TABLE patients ADD COLUMN IF NOT EXISTS %I TEXT;',
                    col
                );
            END LOOP;
        END
        $$;

    """)
    conn.commit()

    cursor.close()
    conn.close()