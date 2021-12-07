import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { MessageFormComponent } from './components/message-form/message-form.component';
import { SentMessageComponent } from './components/sent-message/sent-message.component';
import { RecvMessageComponent } from './components/recv-message/recv-message.component';
import { ChatComponent } from './components/chat/chat.component';
import { MessagesViewComponent } from './components/messages-view/messages-view.component';
import { RecvMessageTextComponent } from './components/recv-message-text/recv-message-text.component';
import { FormsModule } from '@angular/forms';
import { RecvMessageLinkComponent } from './components/recv-message-link/recv-message-link.component';
import { RecvMessageTableComponent } from './components/recv-message-table/recv-message-table.component';
import { RecvMessageVideoComponent } from './components/recv-message-video/recv-message-video.component';
import { RecvMessageDictionaryComponent } from './components/recv-message-dictionary/recv-message-dictionary.component';
import { RecvMessageImageComponent } from './components/recv-message-image/recv-message-image.component';
import { RecvMessageListComponent } from './components/recv-message-list/recv-message-list.component';

@NgModule({
  declarations: [
    AppComponent,
    MessageFormComponent,
    SentMessageComponent,
    RecvMessageComponent,
    ChatComponent,
    MessagesViewComponent,
    RecvMessageTextComponent,
    RecvMessageLinkComponent,
    RecvMessageTableComponent,
    RecvMessageVideoComponent,
    RecvMessageDictionaryComponent,
    RecvMessageImageComponent,
    RecvMessageListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule 
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
