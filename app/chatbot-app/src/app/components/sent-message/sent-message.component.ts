import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-sent-message',
  templateUrl: './sent-message.component.html',
  styleUrls: ['./sent-message.component.css']
})
export class SentMessageComponent implements OnInit {
  @Input('message') message:string = ""
  constructor() { }

  ngOnInit(): void {
  }

}
