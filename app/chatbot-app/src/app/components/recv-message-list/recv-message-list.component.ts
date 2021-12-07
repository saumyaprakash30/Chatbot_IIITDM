import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-list',
  templateUrl: './recv-message-list.component.html',
  styleUrls: ['./recv-message-list.component.css']
})
export class RecvMessageListComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
