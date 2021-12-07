import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-recv-message-dictionary',
  templateUrl: './recv-message-dictionary.component.html',
  styleUrls: ['./recv-message-dictionary.component.css']
})
export class RecvMessageDictionaryComponent implements OnInit {
  @Input('data') data:any = ""
  constructor() { }

  ngOnInit(): void {
  }

}
