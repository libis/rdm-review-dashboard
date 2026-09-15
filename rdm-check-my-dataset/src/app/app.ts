import { Component, inject, signal, OnInit } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterOutlet } from '@angular/router';
import { Config } from './services/config';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  private readonly config = inject(Config);
  private readonly http = inject(HttpClient);
  private readonly sanitizer = inject(DomSanitizer);

  protected readonly title = signal('pre-review-checklist-ui');

  protected readonly customHeader = toSignal<SafeHtml | undefined>(
    this.http.get('assets/cmd/header.html', { responseType: 'text' }).pipe(
      map((headerHTML) => this.sanitizer.bypassSecurityTrustHtml(headerHTML))
    ),
    { initialValue: undefined }
  );

  protected readonly customFooter = toSignal<SafeHtml | undefined>(
    this.http.get('assets/cmd/footer.html', { responseType: 'text' }).pipe(
      map((footerHTML) => this.sanitizer.bypassSecurityTrustHtml(footerHTML))
    ),
    { initialValue: undefined }
  );

  ngOnInit(): void {
  }
}
