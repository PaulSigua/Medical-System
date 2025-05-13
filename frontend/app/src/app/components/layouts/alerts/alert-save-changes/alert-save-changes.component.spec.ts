import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertSaveChangesComponent } from './alert-save-changes.component';

describe('AlertSaveChangesComponent', () => {
  let component: AlertSaveChangesComponent;
  let fixture: ComponentFixture<AlertSaveChangesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AlertSaveChangesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlertSaveChangesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
