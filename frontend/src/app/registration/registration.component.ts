import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { RegistrationService } from './registration.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [FormsModule, RouterModule],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {
  loader: boolean = false;
  showAck: boolean = false;
  constructor(private registrationService: RegistrationService){}
  onRegistration(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.loader = true;
      let fd = new FormData();
      fd.append('first_name', data.value.first_name);
      fd.append('last_name', data.value.last_name);
      fd.append('email', data.value.email);
      fd.append('contact_number', data.value.contact);
      fd.append('gender', data.value.gender);
      fd.append('password', data.value.password);
      fd.append('group', 'general_user');
      fd.append('is_deleted', 'False');
      fd.append('username', data.value.username);
      this.registrationService.register_user(fd).subscribe({
        next: data => {
          this.loader = false
          this.showAck = true;
        }
      })
    }
  }
}
