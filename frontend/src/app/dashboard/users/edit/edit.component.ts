import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { UsersService } from '../users.service';
import { Router } from '@angular/router';
import { OfficeService } from '../../../services/office.service';
import { IOfficeDetails } from '../../../interfaces/ioffice-details';

@Component({
  selector: 'app-edit',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './edit.component.html',
  styleUrl: './edit.component.css'
})
export class EditComponent {
  offices: Array<IOfficeDetails> = [];
  loader: boolean = false;
  constructor(private usersSerivce: UsersService,
    private officeService : OfficeService,
    private router: Router){
    this.get_offices();
  }
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
      fd.append('group', data.value.role);
      fd.append('is_deleted', 'False');
      fd.append('username', data.value.username);
      fd.append('office', data.value.organization);
      this.usersSerivce.register_user(fd).subscribe({
        next: data => {
          this.loader = false;
          this.router.navigate(['/dashboard/users/view']);
        }
      })
    }
  }
  get_offices(){
    this.officeService.get_all().subscribe({
      next: data => {
        this.offices = data;
      }
    })
  }

}
