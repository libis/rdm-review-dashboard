import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatasetSelection } from './dataset-selection';

describe('DatasetSelection', () => {
  let component: DatasetSelection;
  let fixture: ComponentFixture<DatasetSelection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatasetSelection],
    }).compileComponents();

    fixture = TestBed.createComponent(DatasetSelection);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
