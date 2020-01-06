import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, NgControlStatus } from '@angular/forms';
import { DataLoaderService } from '../data-loader.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css', '../global-style.css']
})
export class SettingsComponent implements OnInit {

  Form = new FormGroup({
    SilendAlarm: new FormControl(true),
    DisableCamera: new FormControl(false),
    OutLightOnTrig: new FormControl(0),
    OutLightOffTrig: new FormControl(0),
    // RFID: new FormControl('')
  });

  constructor(private dataLoader: DataLoaderService) { }

  ngOnInit() {
  }

  submit() {
    this.dataLoader.updateSettings({
      SilentAlarm: this.Form.controls.SilendAlarm.value,
      OutLightOnTrig: this.Form.controls.OutLightTrig.value,
      OutLightOffTrig: this.Form.controls.OutLightTrig.value,
      DisableCamera: this.Form.controls.DisableCamera.value
    });
  }
}
