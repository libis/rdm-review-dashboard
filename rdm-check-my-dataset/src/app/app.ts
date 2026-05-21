import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Config } from './services/config';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('pre-review-checklist-ui');
  constructor(
    private config: Config,
  ) {
  }
}
