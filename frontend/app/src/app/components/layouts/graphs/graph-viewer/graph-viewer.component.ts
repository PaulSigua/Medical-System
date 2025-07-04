import { Component, Input, SimpleChanges } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { GraphType, PatientService } from '../../../../services/patients/patient.service';

@Component({
  selector: 'app-graph-viewer',
  standalone: false,
  templateUrl: './graph-viewer.component.html',
  styleUrl: './graph-viewer.component.css'
})
export class GraphViewerComponent {

  @Input() patientId!: string;
  @Input() type: GraphType = 'graph6';

  url: SafeResourceUrl | null = null;
  loading = false;
  error: string | null = null;

  constructor(private graphService: PatientService) {}

  ngOnChanges(changes: SimpleChanges) {
    if (changes['patientId'] || changes['type']) this.load();
  }

  private load() {
    this.url = null;
    this.error = null;
    this.loading = true;

    this.graphService.fetchGraph(this.patientId, this.type).subscribe({
      next: u => {
        this.url = u;
        this.loading = false;
      },
      error: () => {
        this.error = 'No se pudo cargar la gráfica';
        this.loading = false;
      }
    });
  }
}
