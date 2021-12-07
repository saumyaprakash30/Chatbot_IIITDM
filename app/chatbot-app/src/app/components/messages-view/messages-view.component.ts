import { Component, Input, OnChanges, OnInit, SimpleChanges,ComponentFactoryResolver, ViewChild, ViewContainerRef } from '@angular/core';
import { RecvMessageDictionaryComponent } from '../recv-message-dictionary/recv-message-dictionary.component';
import { RecvMessageImageComponent } from '../recv-message-image/recv-message-image.component';
import { RecvMessageLinkComponent } from '../recv-message-link/recv-message-link.component';
import { RecvMessageListComponent } from '../recv-message-list/recv-message-list.component';
import { RecvMessageTableComponent } from '../recv-message-table/recv-message-table.component';

import { RecvMessageTextComponent } from '../recv-message-text/recv-message-text.component';
import { RecvMessageVideoComponent } from '../recv-message-video/recv-message-video.component';
import { SentMessageComponent } from '../sent-message/sent-message.component';

@Component({
  selector: 'app-messages-view',
  templateUrl: './messages-view.component.html',
  styleUrls: ['./messages-view.component.css']
})
export class MessagesViewComponent implements OnInit,OnChanges {
  @ViewChild('messageHistory', {read: ViewContainerRef}) container!: ViewContainerRef ;
  @Input() botMessageRecved:Event | undefined
  @Input() botYouMessageRecved:Event | undefined
  messages:any[] = []
  messageClass = RecvMessageTextComponent
  constructor(private componentFactoryResolver: ComponentFactoryResolver) { }
  ngOnChanges(changes: SimpleChanges): void {
    if(changes['botYouMessageRecved']){
      this.addSentMessage(changes['botYouMessageRecved'].currentValue)
    }
    console.log(changes);
    let msg =changes['botMessageRecved'].currentValue
    
    switch (msg.reply_type) {
      case "text":
        this.addTextMessage(msg)
        break;
      case "dictionary":
        this.addDictionaryMessage(msg)
        break;
        case "image":
          this.addImageMessage(msg)
          break;
          case "link":
        this.addLinkMessage(msg)
        break;
        case "list":
        this.addListMessage(msg)
        break;
        case "table":
        this.addTableMessage(msg)
        break;
        case "video":
        this.addVideoMessage(msg)
        break;
      default:
        break;
    }
  }
  
  ngOnInit(): void {
  }
  addSentMessage(message:string){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(SentMessageComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.message);
    
    componentRef.instance.message = message;
    this.messages.push(componentRef)
  }
  addTextMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageTextComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
  addLinkMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageLinkComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
  addDictionaryMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageDictionaryComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
  addImageMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageImageComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }

  addListMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageListComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
  addTableMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageTableComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
  addVideoMessage(data:any){
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(RecvMessageVideoComponent);
    let componentRef = this.container?.createComponent(componentFactory);
    console.log(componentRef.instance.data);
    
    componentRef.instance.data = data;
    this.messages.push(componentRef)
  }
}
