import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AuthService } from '../../../../login/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  username:string = '';
  @Output() onToggle = new EventEmitter<boolean>();
  @Input() toggleValue: boolean = false;
  constructor(private authService: AuthService){}
  onInitToggle(){
    this.toggleValue = !this.toggleValue;
    this.onToggle.emit(this.toggleValue);
  }
  onLogout(){
    this.authService.logout().subscribe({
      next: () => window.location.href = '/',
    });
  }
}
