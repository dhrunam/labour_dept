import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  username:string = '';
  @Output() onToggle = new EventEmitter<boolean>();
  @Input() toggleValue: boolean = false;
  // constructor(private authService: AuthService, private localStorageService: LocalStorageService){
  //   this.username = this.localStorageService.getDetails().related_profile ? this.localStorageService.getDetails().related_profile.name : this.localStorageService.getDetails().username;
  // }
  onInitToggle(){
    this.toggleValue = !this.toggleValue;
    this.onToggle.emit(this.toggleValue);
  }
  // onLogout(){
  //   this.authService.logout().subscribe({
  //     next: () => window.location.href = '/',
  //   });
  // }
}
