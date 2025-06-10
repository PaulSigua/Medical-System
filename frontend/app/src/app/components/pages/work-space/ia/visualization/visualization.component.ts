import { Component, OnInit } from '@angular/core';
import { GraphData } from '../../../../../models/models';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { environment } from '../../../../../../environments/environment.development';

@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent implements OnInit {
  graphList: GraphData[] = [];
  selectedGraphId: string | null = null;
  detectionMessage: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private sanitizer: DomSanitizer
  ) {}

  private sanitizeUrl(relative: string|null|undefined): SafeResourceUrl|null {
    if (!relative) return null;
    // Si ya es absoluta, la usamos tal cual, si no, la completamos:
    const full = relative.startsWith('http')
      ? relative
      : `${environment.BACKEND_URL}${relative}`;
    return this.sanitizer.bypassSecurityTrustResourceUrl(full);
  }

  ngOnInit(): void {
    this.route.queryParamMap.subscribe((qp) => {
      this.detectionMessage = qp.get('detection_message');

      // Construye dinámicamente tu arreglo
      this.graphList = [
        {
          id: 'graph1',
          label: '3D Cerebral',
          title: 'Visualización Cerebral 3D',
          url: this.sanitizeUrl(qp.get('html_url1')),
        },
        {
          id: 'graph2',
          label: 'Diámetros',
          title: 'Diámetros de Clases',
          url: this.sanitizeUrl(qp.get('html_url2')),
        },
        {
          id: 'graph3',
          label: 'Rebanadas',
          title: 'Visualización de Rebanadas',
          url: this.sanitizeUrl(qp.get('html_url3')),
        },
        {
          id: 'graph4',
          label: 'Clasificación',
          title: 'Clasificación de Rebanadas',
          url: this.sanitizeUrl(qp.get('html_url4')),
        },
        {
          id: 'graph5',
          label: 'Gráfica 5',
          title: 'Gráfica 5',
          url: this.sanitizeUrl(qp.get('html_url5')),
        },
        {
          id: 'graph6',
          label: 'Modalidades',
          title: 'Visualización de Modalidades',
          url: this.sanitizeUrl(qp.get('html_url6')),
        },
      ].filter((g) => g.url);

      // Selecciona la primera disponible
      this.selectedGraphId = this.graphList.length
        ? this.graphList[0].id
        : null;
    });
  }
}
