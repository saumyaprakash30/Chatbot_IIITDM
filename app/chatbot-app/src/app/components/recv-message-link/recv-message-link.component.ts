import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-link',
  templateUrl: './recv-message-link.component.html',
  styleUrls: ['./recv-message-link.component.css']
})
export class RecvMessageLinkComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
