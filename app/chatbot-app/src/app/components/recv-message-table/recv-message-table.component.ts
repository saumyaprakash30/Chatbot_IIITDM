import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-table',
  templateUrl: './recv-message-table.component.html',
  styleUrls: ['./recv-message-table.component.css']
})
export class RecvMessageTableComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
