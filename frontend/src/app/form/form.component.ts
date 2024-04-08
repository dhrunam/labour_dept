import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { FormService } from './form.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {
  offices: Array<any> = [];
  districts: Array<any> = [];
  establishments: Array<any> = [];
  agree: boolean = false;
  loader: boolean = false;
  photo: any;
  constructor(private formService: FormService, private router: Router){}
  ngOnInit(): void{
    this.get_districts();
    this.get_establishments();
    this.get_offices();
  }
  get_districts(){
    this.formService.get_districts().subscribe({
      next: data => {
        this.districts = data.results;
      }
    })
  }
  get_establishments(){
    this.formService.get_establishments().subscribe({
      next: data => {
        this.establishments = data.results;
      }
    })
  }
  get_offices(){
    this.formService.get_offices().subscribe({
      next: data => {
        this.offices = data.results;
      }
    })
  }
  getCheck(event: any){
    this.agree = event.target.checked ? true : false;
  }
  photoUpload(event: any){
    if(event.target.files){
      this.photo = event.target.files[0];
    }
  }
  submitForm(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.loader = true;
      let fd = new FormData();
      fd.append('office_location', data.value.district);
      fd.append('registration_status', data.value.registration_type);
      fd.append('full_name_applicant', data.value.full_name);
      fd.append('email_applicant', data.value.email);
      fd.append('photograph_applicant', this.photo);
      fd.append('establishment_name', data.value.establishment_name);
      fd.append('establishment_address', data.value.address);
      fd.append('establishment_pincode', '737101');
      fd.append('situation_of_other_premises', data.value.situation);
      fd.append('establishment_category', data.value.establishment_category);
      fd.append('nature_business', data.value.nature_of_business);
      fd.append('total_emplyee_male_18', data.value.old_male);
      fd.append('total_emplyee_female_18', data.value.old_female);
      fd.append('total_emplyee_other_18', data.value.old_total);
      fd.append('total_emplyee_male_14', data.value.young_male);
      fd.append('total_emplyee_female_14', data.value.young_female);
      fd.append('total_emplyee_other_14', data.value.young_total);
      fd.append('weekly_holidays_name', data.value.weekly_holidays);
      fd.append('is_agreed_terms_and_condition', this.agree ? 'True':'False');
      fd.append('applied_office_details', data.value.office);
      fd.append('employer_parentage_details', '[{"parentage_name":"Test", "designation":"adviseer","permanent_address":"Test","nature_interest":"Test"},{"parentage_name":"Test1", "designation":"adviseer","permanent_address":"Test","nature_interest":"Test"},{"parentage_name":"Test2", "designation":"adviseer","permanent_address":"Test","nature_interest":"Test"}]');
      fd.append('employer_details', '[{"designation":"adviseer","name":"Test","permanent_address":"Test"},{"designation":"adviseer","name":"Test","permanent_address":"Test"}]');
      fd.append('employer_family_member_details', '[{"name":"xyz","age":70.00,"relationship":"Test"},{"name":"adviseer","age":60.6,"relationship":"Test"}]');
      fd.append('management_level_employee_details', '[{"name":"xyz","age":30.00,"relationship":"Test"},{"name":"adviseer","age":40.00,"relationship":"Test"}]');
      this.formService.submit_application(fd).subscribe({
        next: data => {
          this.loader = false;
          this.router.navigate(['/acknowledgement']);
        }
      })
    }
  }
}
