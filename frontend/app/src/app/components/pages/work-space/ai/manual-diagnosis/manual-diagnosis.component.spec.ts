import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManualDiagnosisComponent } from './manual-diagnosis.component';

describe('ManualDiagnosisComponent', () => {
  let component: ManualDiagnosisComponent;
  let fixture: ComponentFixture<ManualDiagnosisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManualDiagnosisComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManualDiagnosisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
