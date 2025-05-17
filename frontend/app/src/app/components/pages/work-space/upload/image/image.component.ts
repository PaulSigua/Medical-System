import { Component } from '@angular/core';
import { Upload } from 'lucide-angular';

@Component({
  selector: 'app-image',
  standalone: false,
  templateUrl: './image.component.html',
  styleUrl: './image.component.css',
})
export class ImageComponent {

  icons = {
    Upload
  }

  fileSelected: boolean = false;
  archivosInfo: { nombre: string; tamano: string }[] = [];
  errorMessage: string = '';
  showUploadZone: boolean = true; 

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.fileSelected = !!input.files && input.files.length > 0;

    if (input.files) {
      const selectedFiles = Array.from(input.files);

      // Filtra los archivos por extensión .nii.gz
      const validFiles = selectedFiles.filter((file) =>
        file.name.endsWith('.nii.gz')
      );

      // Si hay archivos no válidos, mostrar un mensaje de error
      if (validFiles.length < selectedFiles.length) {
        this.errorMessage =
          'Solo se permiten archivos con la extensión .nii.gz';
        this.showUploadZone = true; // Mantener la zona visible si hay archivo no válido
      } else {
        this.errorMessage = ''; // Limpiar mensaje de error si todos son válidos
        this.showUploadZone = false; // Ocultar la zona de carga si el archivo es válido
      }

      // Actualiza la lista de archivos si todos son válidos
      if (validFiles.length > 0) {
        this.archivosInfo = validFiles.map((file) => ({
          nombre: file.name,
          tamano: this.formatearTamano(file.size),
        }));
      }
    }
  }

  private formatearTamano(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }
}
