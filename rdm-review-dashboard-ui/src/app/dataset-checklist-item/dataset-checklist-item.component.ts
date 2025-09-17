import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-dataset-checklist-item',
  templateUrl: './dataset-checklist-item.component.html',
  styleUrls: ['./dataset-checklist-item.component.scss']
})
export class DatasetChecklistItemComponent implements OnInit {
  @Input() id!: string;
  @Input() checked!: boolean;
  @Input() showAutochecks: boolean = false;
  @Input() enabled: boolean = true;
  @Input() label!: string;
  @Input() warning!: string | null;
  @Input() autocheckState: boolean | null = null;
  @Output() checkedChange = new EventEmitter<{id: string, checked: boolean}>();

  get sameAsAutocheck(): boolean | null {
    if (this.autocheckState === null) {
      return null;
    }
    return this.checked === this.autocheckState;
  }
  constructor() { }

  ngOnInit(): void {
  }


  onCheckboxChange() {
    this.checkedChange.emit({id: this.id, checked: this.checked});
  }
}
