import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class DataLoaderService {

  constructor(http: HttpClient) { 

  }

  private fetchNewData(){

  }
}
interface StateData {
  
}