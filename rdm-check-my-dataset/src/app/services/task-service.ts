import { computed, Injectable, signal, Signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import {
  BehaviorSubject,
  takeWhile,
  distinctUntilChanged,
  timer,
  switchMap,
  map,
  Observable,
  of,
} from 'rxjs';
import { ApiService } from './api-service';

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  mainTaskIdFollowed: BehaviorSubject<string | null> = new BehaviorSubject<string | null>(null);
  latestResults: Signal<any | null> = signal(null);
  taskStatuses$: Observable<any | null>;
  taskStatuses: Signal<any | null>;
  tasksStarted: string | null = null;
  taskDescription!: Signal<Map<string, any>>;
  done: Signal<any[]> = signal([]);
  all: Signal<any[]> = signal([]);
  // statuses: Signal<any|null> = signal(null);
  details: Signal<any | null> = signal(null);
  results: Signal<any | null> = signal(null);
  statuses: Signal<Map<string, string>> = signal(new Map());
  constructor(private api: ApiService) {
    this.taskStatuses$ = this.mainTaskIdFollowed.asObservable().pipe(
      distinctUntilChanged(),
      switchMap((orchestratorTaskId) => {
        if (!orchestratorTaskId) {
          return of(null);
        }
        return timer(0, 3000).pipe(
          switchMap(() => this.api.pollResults(orchestratorTaskId)),
          takeWhile((result: any) => {
            if (!result || !result.tasks) {
              return true;
            }
            const allTasksDone = result.tasks.every((task: any) => task.status === 'done');
            return !allTasksDone;
          }, true),
        );
      }),
    );
    this.taskStatuses = toSignal(this.taskStatuses$);
    this.all = computed(() => {
      return this.taskStatuses()?.tasks || [];
    });
    this.done = computed(() =>
      (this.taskStatuses()?.tasks || []).filter((task: any) => task.status === 'done'),
    );
    this.taskDescription = computed(() => {
      let result: Map<string, any> = new Map();
      const ts = this.taskStatuses();
      if (!ts || !ts.details) {
        return result;
      }
      for (let item of ts.details || []) {
        result.set(item.id, item);
      }
      return result;
    });
    this.results = computed(() => {
      let result: Map<string, any> = new Map();
      const ts = this.taskStatuses();
      if (!ts || !ts.tasks) {
        return result;
      }
      for (let item of ts.tasks || []) {
        result.set(item.task_id, item);
      }
      return result;
    });
    this.statuses = computed(() => {
      let result: Map<string, string> = new Map();
      const ts = this.taskStatuses();
      if (!ts || !ts.tasks) {
        return result;
      }
      for (let item of ts.tasks || []) {
        result.set(item.id, item.status);
      }
      return result;
    });
  }


  setTaskToFollow(newId: string | null) {
    console.log('following task', newId);
    this.mainTaskIdFollowed.next(newId);
  }
}
