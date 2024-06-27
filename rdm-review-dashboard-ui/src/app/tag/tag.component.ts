import { Component, OnInit, Input } from '@angular/core';


export namespace Style {
  export enum Color {
    Blue = 'blue',
    Grey = 'grey',
    Red = 'red',
    Primary = 'primary',
    Secondary = 'secondary',
    Warning = 'warning',
    Danger = 'danger',
  }
}

@Component({
  selector: 'app-tag',
  templateUrl: './tag.component.html',
  styleUrls: ['./tag.component.scss']
})
export class TagComponent {
  @Input() text!: string;
  @Input() type!: string | null;
  @Input() color: string = '';

  fontWeight = ""
  constructor() { }



  getColor(): string {
    switch (this.color) {
      case Style.Color.Blue:
        return "text-blue-500"
      case Style.Color.Grey:
        return "text-black-alpha-90"
      case Style.Color.Red:
        return "text-red-500"
      case Style.Color.Primary:
        return "text-blue-500"
      case Style.Color.Secondary:
        return "text-black-alpha-90"
      case Style.Color.Danger:
        return "text-red-500"
      default:
        return "font-medium"
    }
  }

  getIcon(): string {
    let result: string = ""
    switch (this.text) {
      case "Publishing...":
        result = "pi pi-lock";
    }
    switch (this.type) {
      case "support":
        result = "pi pi-flag";
        break;
      case "reviewer":
        result = "pi pi-user";
        break;

    }
    return result;
  }


  getStyle(): string {
    return "flex align-items-center justify-content-center bg-gray-200 font-medium px-2 py-0 m-1" + " " + this.getColor()
  }


}
