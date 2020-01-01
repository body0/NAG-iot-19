import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { DataLoaderService } from '../data-loader.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css', '../global-style.css']
})
export class LoginComponent implements OnInit {

  LoginForm = new FormGroup({
    password: new FormControl('')
  });
  ErrMsg = '';

  constructor(private dataLoader: DataLoaderService) { }

  ngOnInit() {
  }

  login() {
    if (!this.LoginForm.controls.password.valid) { return; }
    const password = this.LoginForm.controls.password.value;
    this.dataLoader.login(password)
    .catch(err => {
      this.ErrMsg = 'Cannot Auth.';
    });
  }

  logout() {
    this.dataLoader.logout();
  }

}
