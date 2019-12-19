import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ActualStateComponent } from './actual-state.component';

describe('ActualStateComponent', () => {
  let component: ActualStateComponent;
  let fixture: ComponentFixture<ActualStateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ActualStateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ActualStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
