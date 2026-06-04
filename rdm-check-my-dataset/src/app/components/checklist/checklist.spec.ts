import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Checklist } from './checklist';

describe('Checklist', () => {
  let component: Checklist;
  let fixture: ComponentFixture<Checklist>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Checklist]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Checklist);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
