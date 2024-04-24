import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthService } from './auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  constructor(private authService: AuthService){}
  onLogin(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      let fd = new FormData();
      fd.append('username', data.value.username);
      fd.append('password', data.value.password);
      fd.append('client', 'api');
      this.authService.login(fd).subscribe({
        next: data => {
          window.location.href = '/dashboard';
        }
      })
    }
  }
}
