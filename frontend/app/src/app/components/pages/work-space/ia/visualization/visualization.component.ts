import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../../../../environments/environment.development';

@Component({
  selector: 'app-visualization',
  standalone: false,
  templateUrl: './visualization.component.html',
  styleUrl: './visualization.component.css',
})
export class VisualizationComponent implements OnInit {
  iframeUrl: SafeResourceUrl | null = null;
  summaryImageUrl: SafeResourceUrl | null = null;
  classDistImageUrl: SafeResourceUrl | null = null;
  isLoading = true;
  error: string | null = null;
  diceScores: any = null;
  allMetrics: any = null;

  constructor(
    private route: ActivatedRoute,
    private sanitizer: DomSanitizer,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      const folderId = params['folder_id'];
      if (folderId) {
        const formData = new FormData();
        formData.append('upload_folder_id', folderId);
        formData.append('framework', 'nnunet');

        this.http
          .post<any>(`${environment.API_URL}/ai/segmentation`, formData)
          .subscribe({
            next: (res) => {
              const fullUrl = `${environment.BACKEND_URL}${res.segmentation_url}`;
              this.iframeUrl =
                this.sanitizer.bypassSecurityTrustResourceUrl(fullUrl);
              this.summaryImageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.BACKEND_URL}${res.summary_image_url}`);
              this.classDistImageUrl = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.BACKEND_URL}${res.class_distribution_url}`);
              this.diceScores = res.metrics?.dice_score;
              this.allMetrics = res.metrics?.all_metrics;
              this.isLoading = true;
            },
            error: (err) => {
              this.error =
                err.error?.detail || 'Error al cargar la segmentación.';
              this.isLoading = false;
            },
          });
      } else {
        this.error = 'No se proporcionó el folder_id.';
        this.isLoading = false;
      }
    });
  }

  onIframeLoad() {
    this.isLoading = false;
  }
}
