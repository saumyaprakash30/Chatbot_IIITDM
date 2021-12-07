import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  public clickedEvent: Event | undefined;
  public clickedYouMessageEvent: Event | undefined;

  constructor() { }

  ngOnInit(): void {
  }

  childBoTMessageRecved(event: Event){
    this.clickedEvent = event;
  }
  childYouMessageRecved(message: Event){
    this.clickedYouMessageEvent = message;
    console.log("message",message);
    
  }
}
