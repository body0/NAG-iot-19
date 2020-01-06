import { Component, OnInit, OnDestroy } from '@angular/core';
import { DataLoaderService, StateData } from '../data-loader.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-actual-state',
  templateUrl: './actual-state.component.html',
  styleUrls: ['./actual-state.component.css', '../global-style.css']
})
export class ActualStateComponent implements OnDestroy {

  Lights: { name: string, status: boolean }[] = [];
  State: StateData;
  Destructor: Subscription;

  constructor(private dataLoader: DataLoaderService) {
    dataLoader.subscribeOnNewStateLoad(state => {
      this.State = state;
      const lights = [];
      Object.getOwnPropertyNames(state.Lights)
        .forEach(lightName => {
          lights.push({
            name: lightName,
            status: state.Lights[lightName].status
          });
        });
      lights.sort((a: { name: string, status: boolean }, b: { name: string, status: boolean }) => {
        if (a.name < b.name) { return -1; }
        if (a.name > b.name) { return 1; }
        return 0;
      });
      this.Lights = lights;
    });
  }

  ngOnDestroy() {
    //this.Destructor.unsubscribe();
  }
}
