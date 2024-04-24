import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  onLogin(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      console.log(data.value.username, data.value.password );
    }
  }
}
