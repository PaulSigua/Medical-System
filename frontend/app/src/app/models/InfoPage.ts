import { Brain } from "lucide-angular";

export class InfoPage {
    name: string = 'Cranius AI';
    title: string = 'Cranius AI - Tu asistente de IA';
    description: string = 'CraniusAI es un asistente de IA que te ayuda a predecir el cancer cerebral y que te ayuda a encontrar la mejor forma de tratarlo.';
    address_street: string = 'Av. Calle Vieja';
    address_city: string = 'Cuenca';
    address_country: string = 'Ecuador';
    hostname: string = 'ups.edu.ec';
    email: string = 'ai@ups.edu.ec';
    logo: typeof Brain = Brain;
}