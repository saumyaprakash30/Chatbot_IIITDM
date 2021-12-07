import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';


const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  constructor(private http:HttpClient) { }

  getReply(message:string){
    const api = environment.url + "/?message="+message
    return this.http.get(api);

  }
}
