import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { DataLoaderService } from '../data-loader.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css', '../global-style.css']
})
export class SettingsComponent implements OnInit {

  Form = new FormGroup({
    SilendAlarm: new FormControl(true),
    // RFID: new FormControl('')
  });

  constructor(private dataLoader: DataLoaderService) { }

  ngOnInit() {
  }

  submit() {
    this.dataLoader.updateSettings({
      SilentAlarm: this.Form.controls.SilendAlarm.value
    });
  }
}
