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

}
