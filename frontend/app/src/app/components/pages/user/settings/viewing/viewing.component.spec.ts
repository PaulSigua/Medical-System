import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewingComponent } from './viewing.component';

describe('ViewingComponent', () => {
  let component: ViewingComponent;
  let fixture: ComponentFixture<ViewingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ViewingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
