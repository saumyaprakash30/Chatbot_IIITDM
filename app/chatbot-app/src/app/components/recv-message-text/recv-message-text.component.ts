import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-text',
  templateUrl: './recv-message-text.component.html',
  styleUrls: ['./recv-message-text.component.css']
})
export class RecvMessageTextComponent implements OnInit {

  @Input('data') data:any = ""
  
  constructor() { }

  ngOnInit(): void {
  }

}
