import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {
  private filenameSource = new BehaviorSubject<string | null>(null);
  filename$ = this.filenameSource.asObservable();

  setFilename(name: string) {
    this.filenameSource.next(name);
  }
}