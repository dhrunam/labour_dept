import { Component } from '@angular/core';
import { SignupService } from './signup.service';

import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule,RouterModule,CommonModule],
  templateUrl: './signup.component.html',
  styleUrl: './signup.component.css'
})
export class SignupComponent {
  selected_gender: string = '';
  site_key: string = '';
  id_proof: any;
  photo: any;
  constructor(private registrationService: SignupService, private router: Router) {
    // this.site_key = CAPTCHA_SITE_KEY;
  }

  onFormSubmit(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      let fd = new FormData();
      // const contact:any = this.contact;
     
      fd.append('first_name', data.value.first_name);
      fd.append('last_name', data.value.last_name);
      fd.append('email', data.value.email);
      fd.append('contact_number', data.value.contact);
      // fd.append('gender', data.value.gender);
      // fd.append('id_proof', this.id_proof);
      // fd.append('password', sha('sha256').update(data.value.pswd).digest('hex'));
      fd.append('password', data.value.pswd);
      fd.append('group', 'general_user');
      fd.append('is_deleted', 'False');
      // fd.append('document_type', data.value.doc_type);
      console.log('Password:'+ fd.get('password'))
      this.registrationService.signup(fd).subscribe({
        next: (success: boolean) => {
          if (success)
          {
            this.router.navigate(['/signup-success']);
          }
         
          // this.success.emit({status: true, ackMessage: 'success'});
        }
      })
    }
  }
  onGetIdProof(event:any){
    if(event.target.files){
      this.id_proof = event.target.files[0];
    }
  }
}
