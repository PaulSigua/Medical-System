import { Component, OnInit } from '@angular/core';
import { GraphData } from '../../../../../models/models';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { environment } from '../../../../../../environments/environment.development';
import { SegmentationService } from '../../../../../services/graphs/segmentation.service';

@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent implements OnInit {
  iframeUrl: SafeResourceUrl | null = null;
  patientId: string | null = null;
  isLoading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
    private segmentationService: SegmentationService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      this.patientId = params['patient_id'];
      if (this.patientId) {
        const fullUrl = `${environment.BACKEND_URL}/static/${this.patientId}/html/segmentation_result.html`;
        this.iframeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(fullUrl);
        this.isLoading = true;
      }
    });
  }

  onIframeLoad() {
    this.isLoading = false;
  }
}
