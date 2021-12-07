import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-image',
  templateUrl: './recv-message-image.component.html',
  styleUrls: ['./recv-message-image.component.css']
})
export class RecvMessageImageComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
