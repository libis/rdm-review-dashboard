import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-dataset-checklist-item',
  templateUrl: './dataset-checklist-item.component.html',
  styleUrls: ['./dataset-checklist-item.component.scss']
})
export class DatasetChecklistItemComponent implements OnInit {
  @Input() checkboxId!: string;
  @Input() checkboxLabel!: string;
  @Input() checkboxEnabled: boolean = true;
  @Input() checkboxChecked!: boolean;
  @Input() showAutochecks: boolean = false;
  @Input() autocheckResultChecked: boolean | null = null;
  @Input() autocheckResultMessages!: {warning: string | null};
  @Output() checkedChange = new EventEmitter<{id: string, checked: boolean}>();

  get checkboxSameAsAutocheck(): boolean | null {
    if (this.autocheckResultChecked === null) {
      return null;
    }
    return this.checkboxChecked === this.autocheckResultChecked;
  }

  constructor() { }

  ngOnInit(): void {
  }


  onCheckboxChange() {
    this.checkedChange.emit({id: this.checkboxId, checked: this.checkboxChecked});
  }
}
