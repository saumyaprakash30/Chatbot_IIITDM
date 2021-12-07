import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-video',
  templateUrl: './recv-message-video.component.html',
  styleUrls: ['./recv-message-video.component.css']
})
export class RecvMessageVideoComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
