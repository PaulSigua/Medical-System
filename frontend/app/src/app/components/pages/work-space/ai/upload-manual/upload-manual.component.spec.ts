import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadManualComponent } from './upload-manual.component';

describe('UploadManualComponent', () => {
  let component: UploadManualComponent;
  let fixture: ComponentFixture<UploadManualComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UploadManualComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadManualComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
