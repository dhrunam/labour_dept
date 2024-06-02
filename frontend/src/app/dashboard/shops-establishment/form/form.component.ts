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
  employer_parentage_details: Array<any> = [];
  employer_details: Array<any> = [];
  employer_family_member_details: Array<any> = [];
  management_level_employee_details: Array<any> = [];
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
  employerParentageDetails(key: string, data: any){
    if(key === 'add'){
      if(data.employer_parentage_name === '' && data.employer_parentage_desg  === '' && data.employer_parentage_addr === '' && data.employer_parentage_interest === ''){
        alert('Please enter values to the corresponding fields')
      }
      else{
        this.employer_parentage_details.push({
          "parentage_name": data.employer_parentage_name,
          "designation": data.employer_parentage_desg || 'N/A',
          "permanent_address": data.employer_parentage_addr || 'N/A',
          "nature_interest": data.employer_parentage_interest || 'N/A',
        })
      }
    }
    else{
      let index = this.employer_parentage_details.findIndex(i => i.parentage_name === data.employer_parentage_name);
      if(index >= 0){
        this.employer_parentage_details.splice(index, 1);
      }
    }
  }
  employerDetails(key: string, data: any){
    if(key === 'add'){
      if(data.employer_name === '' && data.employer_desg === '' && data.employer_addr === ''){
        alert('Please enter values to the corresponding fields')
      }
      else{
        this.employer_details.push({
          "name": data.employer_name,
          "designation": data.employer_desg || 'N/A',
          "permanent_address": data.employer_addr || 'N/A'
        })
      }
    }
    else{
      let index = this.employer_details.findIndex(i => i.name === data.employer_name);
      if(index >= 0){
        this.employer_details.splice(index, 1);
      }
    }
  }
  employerFamilyMemberDetails(key: string, data: any){
    if(key === 'add'){
      if(data.employer_family_name === '' && data.employer_family_age === '' && data.employer_family_rel === '' && data.employer_family_gender === ''){
        alert('Please enter values to the corresponding fields')
      }
      else{
        this.employer_family_member_details.push({
          "name": data.employer_family_name,
          "age": data.employer_family_age || 'N/A',
          "gender": data.employer_family_gender || 'N/A',
          "relationship": data.employer_family_rel || 'N/A'
        })
      }
    }
    else{
      let index = this.employer_family_member_details.findIndex(i => i.name === data.employer_family_name);
      if(index >= 0){
        this.employer_family_member_details.splice(index, 1);
      }
    }
  }
  managementEmployeeDetails(key: string, data: any){
    if(key === 'add'){
      if(data.employer_management_name === '' && data.employer_management_age === '' && data.employer_management_rel === '' && data.employer_management_gender === ''){
        alert('Please enter values to the corresponding fields')
      }
      else{
        this.management_level_employee_details.push({
          "name": data.employer_management_name,
          "age": data.employer_management_age || 'N/A',
          "gender": data.employer_management_gender || 'N/A',
          "relationship": data.employer_management_rel || 'N/A'
        })
      }
    }
    else{
      let index = this.management_level_employee_details.findIndex(i => i.name === data.employer_management_name);
      if(index >= 0){
        this.management_level_employee_details.splice(index, 1);
      }
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
      fd.append('full_name_applicant', data.value.middle_name ? `${data.value.first_name} ${data.value.middle_name} ${data.value.last_name}` :  `${data.value.first_name} ${data.value.last_name}`);
      fd.append('email_applicant', data.value.email);
      fd.append('photograph_applicant', this.photo);
      fd.append('establishment_name', data.value.establishment_name);
      fd.append('establishment_address', data.value.address);
      fd.append('establishment_pincode', '737101');
      fd.append('situation_of_other_premises', data.value.situation);
      fd.append('establishment_category', data.value.establishment_category);
      fd.append('nature_business', data.value.nature_of_business);
      fd.append('total_emplyee_male_18', '0');
      fd.append('total_emplyee_female_18', '0');
      fd.append('total_emplyee_other_18', data.value.old_total);
      fd.append('total_emplyee_male_14', '0');
      fd.append('total_emplyee_female_14', '0');
      fd.append('total_emplyee_other_14', data.value.young_total);
      fd.append('weekly_holidays_name', data.value.weekly_holidays);
      fd.append('is_agreed_terms_and_condition', this.agree ? 'True':'False');
      fd.append('applied_office_details', data.value.office);
      fd.append('employer_parentage_details', JSON.stringify(this.employer_parentage_details));
      fd.append('employer_details', JSON.stringify(this.employer_details));
      fd.append('employer_family_member_details', JSON.stringify(this.employer_family_member_details));
      fd.append('management_level_employee_details', JSON.stringify(this.management_level_employee_details));
      this.formService.submit_application(fd).subscribe({
        next: data => {
          this.loader = false;
          this.router.navigate(['/dashboard/shops-establishment/acknowledgement']);
        }
      })
    }
  }
}
