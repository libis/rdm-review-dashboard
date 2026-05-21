import { Component, Signal, Output, EventEmitter, signal, computed} from '@angular/core';
import { BehaviorSubject, Subscription} from 'rxjs';
import { AccordionModule } from 'primeng/accordion';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { CardModule } from 'primeng/card';
import { AvatarModule } from 'primeng/avatar';
import { ProgressBarModule } from 'primeng/progressbar';
import { TaskService } from '../../services/task-service';


@Component({
  selector: 'app-task-status',
  imports: [AvatarModule, CardModule, AccordionModule, ButtonModule, ProgressSpinnerModule, ProgressBarModule],
  templateUrl: './task-status.html',
  styleUrl: './task-status.scss',
})
export class TaskStatus {
  datasetId: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  checklistStatuses: string[] = [];
  taskStatuses: Signal<any>;
  tasksStarted: any | null = null;
  @Output() newTaskResultsEvent = new EventEmitter<any|null>();
  @Output() newTaskDetailsEvent = new EventEmitter<any|null>();
  subscription!: Subscription;
  numTasksDone: Signal<number> = signal(-1);
  numTasksAll: Signal<number> = signal(-1);
  constructor(
    private router: Router,
    private tasks: TaskService
  ) {
    this.taskStatuses = computed( () => this.tasks.taskStatuses())
    this.numTasksAll = computed(()=>
      {console.log("all tasks: ", this.tasks.all()?.length);
        return this.tasks.all()?.length})
    this.numTasksDone = computed(()=>
      { console.log("done tasks", this.tasks.done()?.length);
        return this.tasks.done()?.length})
    this.tasks.taskStatuses$.subscribe(
      (taskStatuses) => {
        if (taskStatuses===null) {
          console.log("redirecting to select")
          this.router.navigate(['select']);
        }
      }
    )
  }

}
