import { Component } from '@angular/core';
import { ArrowLeft, FileDown, Printer } from 'lucide-angular';

@Component({
  selector: 'app-terms',
  standalone: false,
  templateUrl: './terms.component.html',
  styleUrl: './terms.component.css'
})
export class TermsComponent {
  currentYear: number = new Date().getFullYear();
  icons = {
    Printer,
    FileDown,
    ArrowLeft
  }

  onPrint(): void {
    window.print();
  }

  onDownloadPDF(): void {
    // Aquí podrías integrar jsPDF o redirigir a tu endpoint de PDF
    console.log('Descargando PDF...');
  }
}
