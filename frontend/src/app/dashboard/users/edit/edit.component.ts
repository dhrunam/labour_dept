import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { UsersService } from '../users.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './edit.component.html',
  styleUrl: './edit.component.css'
})
export class EditComponent {
  loader: boolean = false;
  constructor(private usersSerivce: UsersService, private router: Router){}
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
      this.usersSerivce.register_user(fd).subscribe({
        next: data => {
          this.loader = false;
          this.router.navigate(['/dashboard/users/view'])
        }
      })
    }
  }
}
