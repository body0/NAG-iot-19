import { Component, OnInit } from '@angular/core';
import { DataLoaderService, LightStatus } from '../data-loader.service';

@Component({
  selector: 'app-statistic',
  templateUrl: './statistic.component.html',
  styleUrls: ['./statistic.component.css', '../global-style.css']
})
export class StatisticComponent implements OnInit {

  Lights: LightStatus[] = [];

  constructor(private dataLoader: DataLoaderService) {
    
   }

  ngOnInit() {
  }

  turnOnLight(lightName): void {

  }

}
