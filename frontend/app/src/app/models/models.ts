import { SafeResourceUrl } from "@angular/platform-browser";

export class Users {
    id?: number;
    name?: String;
    last_name?: String;
    username?: String;
    password?: String;
    agree_terms?: boolean;
    phone?: String;
    specialty?: String;
}

export class UpdateUser {
    name?: String;
    last_name?: String;
    username?: String;
    phone?: String;
    specialty?: String;
}

export class Patients {
    user_id?: number
    patient_id?: string
    numero_historia_clinica?: string
    survey_completed?: boolean;
    t1ce_path?: string
    t2_path?: string
    flair_path?: string
    coincidenciaIA?: 'baja' | 'media' | 'alta';
}

export interface GraphData {
  id: string;
  title: string;
  label: string;
  url: SafeResourceUrl | null;
}

export interface ReportStatistics {
  total_predictions: number;
  total_patients: number;
  last_prediction: string | null;
}