import { Component, OnInit, Input } from '@angular/core';
@Component({
  selector: 'app-avatar',
  templateUrl: './avatar.component.html',
  styleUrls: ['./avatar.component.scss']
})
export class AvatarComponent {

  constructor() { }
  @Input() name!: string;



  avatarLabel(): string {
    return this.name;
  }

}
