import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { DataLoaderService } from '../data-loader.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches)
    );

  IsLogin = false;

  constructor(
    private breakpointObserver: BreakpointObserver,
    private dataLoader: DataLoaderService,
    private router: Router) {
    dataLoader.subscribeOnLoginChange(state => {
      this.IsLogin = state;
    });
  }

  logOut() {
    this.dataLoader.logout();
  }

  changeRoute(newRoute){
    this.router.navigate([newRoute]);
  }

}
