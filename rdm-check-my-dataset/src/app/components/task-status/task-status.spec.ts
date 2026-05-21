import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskStatus } from './task-status';

describe('TaskStatus', () => {
  let component: TaskStatus;
  let fixture: ComponentFixture<TaskStatus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskStatus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskStatus);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
