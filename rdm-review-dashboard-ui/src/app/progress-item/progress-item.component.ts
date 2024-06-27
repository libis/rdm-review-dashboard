import { Component, Input, OnInit } from '@angular/core';
import { Router } from "@angular/router";

@Component({
  selector: 'app-progress-item',
  templateUrl: './progress-item.component.html',
  styleUrls: ['./progress-item.component.scss']
})
export class ProgressItemComponent implements OnInit {

  @Input() name: string = '';
  @Input() description: string = '';
  @Input() icon: string = 'pi-question';
  @Input() active: boolean = false;
  @Input() enabled: boolean = false;
  @Input() linkTo: string = '/';


  constructor(private router: Router) {
  }

  ngOnInit(): void {
  }

  getIconClass(): string {
    return `${this.icon} ${this.getTextClass()} text-2xl md:text-4xl mb-2 md:mb-0 mr-0 md:mr-3 `;
  }

  getBorderClass(): string {
    return `${this.getCardColor()} flex flex-column md:flex-row  border-${this.getBorderWidth()} border-round p-3 align-items-center z-1 flex-auto border-${this.getBorderColor()} shadow-3`;

  }

  getCardColor(): string {
    return this.enabled ? 'surface-card' : 'surface-100'

  }

  getTextClass(): string {
    return `text-${this.getTextColor()} `;

  }

  getBorderWidth(): string {
    return this.enabled && this.active ? '2' : '1'

  }

  getTextColor(): string {
    return !this.enabled ? '500' : this.active ? 'blue-500' : 'green-500';
  }
  getBorderColor(): string {
    return !this.enabled ? '300' : this.active ? 'blue-500' : '100';
  }

}
