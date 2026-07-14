import { Component, Input } from '@angular/core';
import { TooltipModule } from 'primeng/tooltip';

@Component({
  selector: 'app-checklist-item',
  standalone: true,
  imports: [TooltipModule],
  templateUrl: './checklist-item.html',
  styleUrl: './checklist-item.scss',
})
export class ChecklistItem {
  @Input() taskStatus!: string | null;
  @Input() taskResults!: any | null;
  @Input() checkboxId!: string;
  @Input() checkboxDetails!: any;
  @Input() checkboxChecked!: boolean | null;
  @Input() helptext!: string | null;
  helpVisible: boolean = false;

  isAutocheckChecked() {
    return this.taskResults?.result;
  }

  getAutocheckWarning(): string | undefined {
    return this.taskResults?.warning || undefined;
  }
  getHelpText() {
    return null;
  }
  showHelp() {
    let helpText = this.getHelpText();
    if (helpText) {
      console.log(helpText);
      this.helpVisible = true;
    }
  }
  getNoResultWarning(): string | undefined {
    return this.checkboxDetails?.no_result_warning || 'This requirement could not be automatically validated, please check its correctness manually.';
  }
}
