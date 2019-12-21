import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Observer, Subject, Subscription } from 'rxjs';
import { environment } from '../environments/environment';
import io from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class DataLoaderService {

  private static readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Accept: 'application/json'
    })
  };
  private static SocketUrl = environment.changeWebSocketBaseUrl;
  private static ApiBase = environment.apiBaseUrl;

  private NewState = new Subject<StateData>();
  private LastState: StateData;
  /*
    Load house state on creation
    Start lisening on socket for new data event, then load (by busic http tequest) new home state
    Start lisening on socket for other type of event (system & user event)
   */

  constructor(private Http: HttpClient) {
    this.loadNewData();

    // const ws = new WebSocket(DataLoaderService.SocketUrl);
    const ws = io.connect(DataLoaderService.SocketUrl);
    ws.on('connect', () => {
      console.log('Socket open');
    });

    ws.on('NEW_STATE_AVAILIBLE', (_) => {
      this.loadNewData();
    });
    const observable: Observable<any> = Observable.create((obs: Observer<MessageEvent>) => {
      ws.on('EVENT_EMITED', pld => {
        obs.next(pld);
      });
      ws.on('disconnect', msg => {
        console.log('Connection close', msg);
        obs.complete();
      });
    });
    observable.subscribe(pld => {
      console.log(pld);
    });
  }

  public subscribeOnNewStateLoad(callback: (state: StateData) => void): Subscription {
    if (this.LastState) {
      callback(this.LastState);
    }
    return this.NewState.subscribe(callback);
  }
  public sendData(data: StateData) {

  }

  private loadNewData() {
    this.Http.get(DataLoaderService.ApiBase + '/state')
      .toPromise()
      .then((body: any) => {
        console.log(body);
        this.NewState.next(body);
        this.LastState = body;
      })
      .catch(err => {
        console.warn('Cannot load house state.', err);
      });
  }
}


export interface StateData {
  Lights: Record<string, LightStatus>;
  Gate: {
    status: boolean,
    lastOpened: string
  };
  LastSuccesfullAuth: string;
  LastFailedAuth: string;
  LightLum: number;
}
export interface LightStatus {
  status: boolean;
}
