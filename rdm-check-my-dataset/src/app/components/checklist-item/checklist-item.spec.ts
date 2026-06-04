import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ChecklistItem } from './checklist-item';

describe('ChecklistItem', () => {
  let component: ChecklistItem;
  let fixture: ComponentFixture<ChecklistItem>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChecklistItem],
    }).compileComponents();

    fixture = TestBed.createComponent(ChecklistItem);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
