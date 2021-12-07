import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ChatbotService } from 'src/app/services/chatbot.service';

@Component({
  selector: 'app-message-form',
  templateUrl: './message-form.component.html',
  styleUrls: ['./message-form.component.css']
})
export class MessageFormComponent implements OnInit {
  
  inputMessage:string = ""
  sentButtonDisable:boolean = true

  @Output() botMessage = new EventEmitter<Event>();
  @Output() youMessage = new EventEmitter<Event>();
  constructor(private _chatbotService:ChatbotService) { }

  ngOnInit(): void {
  }
  sendMessage(){
    let message = this.inputMessage
    if (message.length>0)
    {
      this.addYouMessage(message)
      this._chatbotService.getReply(message).subscribe((response)=>{
        // console.log(response);
        this.addBotMessage(response)
        this.inputMessage = ""
      })
      
      // this._chatbotService.getReply(message).then((response)=>{
      //     this.addBotMessage(response)
      //     this.inputMessage = ""
      // })


    }
    else{
      
    }
  }

  addBotMessage(data:any){
    this.botMessage.emit(data)
  }

  addYouMessage(message:any){
    this.youMessage.emit(message)
  }


}
