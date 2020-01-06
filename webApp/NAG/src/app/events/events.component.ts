import { Component, OnInit } from '@angular/core';
import { DataLoaderService } from '../data-loader.service';

@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.css', '../global-style.css']
})
export class EventsComponent implements OnInit {

  EventList = [];

  constructor(private dataLoader: DataLoaderService) {
    dataLoader.subscribeOnNewEventsLoad(eventList => {
      console.log('events', eventList)
      this.EventList = eventList;
    });
  }

  ngOnInit() {
  }

}
