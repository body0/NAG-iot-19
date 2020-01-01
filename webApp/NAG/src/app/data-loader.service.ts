import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Observer, Subject, Subscription } from 'rxjs';
import { environment } from '../environments/environment';
import io from 'socket.io-client';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class DataLoaderService {

  private static readonly HttpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Accept: 'application/json'
    })
  };
  private static readonly SocketUrl = environment.changeWebSocketBaseUrl;
  private static readonly ApiBase = environment.apiBaseUrl;
  private static readonly MaxEventListLength = 30;

  private NewEvent = new Subject<Event[]>();
  private ElentList: Event[];
  private NewState = new Subject<StateData>();
  private State: StateData;
  private NewSettings = new Subject<SettingsState>();
  private Settings: SettingsState;

  private IsLogin = new Subject<boolean>();
  private Token = null;
  /*
    Load house state on creation
    Start lisening on socket for new data event, then load (by busic http tequest) new home state
    Start lisening on socket for other type of event (system & user event)
   */

  constructor(
    private Http: HttpClient,
    private router: Router) {
    // this.loadAll();

    const ws = io.connect(DataLoaderService.SocketUrl);
    ws.on('connect', () => {
      console.log('Socket open');

      ws.on('NEW_STATE_AVAILIBLE', (_) => {
        this.loadNewStateData();
      });
      /* ws.on('EVENT_EMITED', pld => {
        const event: Event = JSON.parse(pld);
        this.addEvent(event);
      }); */
      ws.on('EVENT_EMITED', pld => {
        this.loadAllEvents();
      });
    });

    // == TEST ==
    /* this.updateSettings({
      SilentAlarm: true
    })
      .then(pld => {
        console.log('POST', pld);
      })
      .catch(e => {
        console.log('POSE ERR:', e);
      }); */
  }

  public subscribeOnLoginChange(callback: (state: boolean) => void): Subscription {
    if (this.Token) {
      callback(true);
    } else {
      callback(false);
    }
    return this.IsLogin.subscribe(callback);
  }
  public subscribeOnNewStateLoad(callback: (state: StateData) => void): Subscription {
    if (this.State) {
      callback(this.State);
    }
    return this.NewState.subscribe(callback);
  }
  public subscribeOnNewSettingsLoad(callback: (state: SettingsState) => void): Subscription {
    if (this.Settings) {
      callback(this.Settings);
    }
    return this.NewSettings.subscribe(callback);
  }

  public updateSettings(settings: SettingsState) {
    const publishedSettings = {
      SilentAlarm: settings.SilentAlarm
    };

    return this.Http.post(
      DataLoaderService.ApiBase + '/settingsUpdate',
      publishedSettings,
      DataLoaderService.HttpOptions)
      .toPromise();
  }

  public async login(password: string) {
    const body = {
      password
    };
    const token: any = await this.Http.post(
      DataLoaderService.ApiBase + '/login',
      body,
      DataLoaderService.HttpOptions)
      .toPromise();
    console.log('[INFO]: token loaded');
    this.Token = token.token;
    this.loadAll();
    this.IsLogin.next(true);
    this.router.navigate(['/state']);
  }
  public logout() {
    this.Token = null;
    this.IsLogin.next(false);
    this.router.navigate(['/login']);
  }

  private getAuthHeder() {
    if (!this.Token) {
      throw new Error('No token awailible');
    }
    return {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        Accept: 'application/json',
        Authorization: 'Bearer ' + this.Token,
      })
    };
  }

  private addEvent(event: Event) {
    if (!this.ElentList) { // "bug" waiting to waiting to happen
      return;
    }
    while (this.ElentList.length > DataLoaderService.MaxEventListLength) {
      this.ElentList.pop();
    }
    this.ElentList.push(event);
    this.NewEvent.next(this.ElentList);
  }

  private loadAll() {
    this.loadNewStateData();
    this.loadSettings();
    this.loadAllEvents();
  }

  private loadAllEvents() {
    this.Http.get(DataLoaderService.ApiBase + '/events')
      .toPromise()
      .then((body: any) => {
        console.log(body);
        this.ElentList = body;
        this.NewEvent.next(body);
      })
      .catch(err => {
        console.warn('Cannot load house state.', err);
      });
  }

  private loadSettings() {
    this.Http.get(DataLoaderService.ApiBase + '/settings')
      .toPromise()
      .then((body: any) => {
        console.log(body);
        this.Settings = body;
        this.NewSettings.next(body);
      })
      .catch(err => {
        console.warn('Cannot load house state.', err);
      });
  }

  private loadNewStateData() {
    this.Http.get(DataLoaderService.ApiBase + '/state', this.getAuthHeder())
      .toPromise()
      .then((body: any) => {
        console.log(body);
        this.NewState.next(body);
        this.State = body;
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

export interface SettingsState {
  SilentAlarm: boolean;
}

export interface Event {
  Name: string;
  Type: string;
  Pld: string;
  Timestamp: string;
}