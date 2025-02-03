import { Component, ViewChild, ElementRef } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { FormService } from './form.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { from } from 'rxjs';
import { OfficeService } from '../../../services/office.service';
import { IOfficeDetails } from '../../../interfaces/ioffice-details';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {
  @ViewChild('employer_parentage_name') employerParentageName!: ElementRef;
  @ViewChild('employer_parentage_desg') employerParentageDesg!: ElementRef;
  @ViewChild('employer_parentage_addr') employerParentageAddr!: ElementRef;
  @ViewChild('employer_parentage_interest') employerParentageInterest!: ElementRef;

  @ViewChild('employer_name') employerName!: ElementRef;
  @ViewChild('employer_desg') employerDesg!: ElementRef;
  @ViewChild('employer_addr') employerAddr!: ElementRef;

  @ViewChild('employer_family_name') employerFamilyName!: ElementRef;
  @ViewChild('employer_family_age') employerFamilyAge!: ElementRef;
  @ViewChild('employer_family_gender') employerFamilyGender!: ElementRef;
  @ViewChild('employer_family_rel') employerFamilyRel!: ElementRef;

  @ViewChild('employer_management_name') employerManagementName!: ElementRef;
  @ViewChild('employer_management_age') employerManagementAge!: ElementRef;
  @ViewChild('employer_management_gender') employerManagementGender!: ElementRef;
  @ViewChild('employer_management_rel') employerManagementRel!: ElementRef;

 
  offices: Array<IOfficeDetails> = [];
  districts: Array<any> = [];
  establishments: Array<any> = [];
  employer_parentage_details: Array<any> = [];
  employer_details: Array<any> = [];
  employer_family_member_details: Array<any> = [];
  management_level_employee_details: Array<any> = [];
  agree: boolean = false;
  loader: boolean = false;
  photo: any;
  trade_licence: any;
  constructor(private formService: FormService, 
    private router: Router, 
    private toaster:ToastrService,
    private officeService:OfficeService,
  ){}
  ngOnInit(): void{
    this.get_districts();
    this.get_establishments();
   
  }
  get_districts(){
    this.formService.get_districts().subscribe({
      next: data => {
        this.districts = data.results;
      }
    })
  }
  onDistrictChange(event:any)
  {
    const district_id=event.target.value;
    this.get_offices(district_id);
  }
  get_establishments(){
    this.formService.get_establishments().subscribe({
      next: data => {
        this.establishments = data.results;
      }
    })
  }
  get_offices(district:number){
    this.officeService.get_all_by_district(district).subscribe({
      next: data => {
        this.offices = data;
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

  tradeLicenceUpload(event: any){
    if(event.target.files){
      this.trade_licence = event.target.files[0];
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

    // Clear input fields after the method call
  this.employerParentageName.nativeElement.value = '';
  this.employerParentageDesg.nativeElement.value = '';
  this.employerParentageAddr.nativeElement.value = '';
  this.employerParentageInterest.nativeElement.value = '';
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

  this.employerName.nativeElement.value = '';
  this.employerDesg.nativeElement.value = '';
  this.employerAddr.nativeElement.value = '';
 
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

  this.employerFamilyName.nativeElement.value = '';
  this.employerFamilyAge.nativeElement.value = '';
  this.employerFamilyGender.nativeElement.value = '';
  this.employerFamilyRel.nativeElement.value = '';

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

  this.employerManagementName.nativeElement.value = '';
  this.employerManagementAge.nativeElement.value = '';
  this.employerManagementGender.nativeElement.value = '';
  this.employerManagementRel.nativeElement.value = '';
  }
  submitForm(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      console.log('employer_parentage_details:')
      console.log(JSON.stringify(this.employer_parentage_details))
      // if(this.employer_parentage_details.length<=0)
      // {
      //   this.loader = false;
      //   alert('Please enter Employer and Parentage Details.')
      //   return;
      // }

      // if(this.employer_details.length<=0)
      //   {
      //     this.loader = false;
      //     alert('Please enter Employer Details.')
      //     return;
      //   }

      // if(this.employer_family_member_details.length<=0)
      //     {
      //       this.loader = false;
      //       alert('Please enter Employer Family Member Details.')
      //       return;
      //     }
      // if(this.management_level_employee_details.length<=0)
      //       {
      //         this.loader = false;
      //         alert('Please enter Management Level Employee Details.')
      //         return;
      //       }
      this.loader = true;
      let fd = new FormData();
      fd.append('application_no_prefix',data.value.reference_no);
      fd.append('office_location', data.value.district);
      fd.append('registration_status', data.value.registration_type);
      fd.append('full_name_applicant', data.value.middle_name ? `${data.value.first_name} ${data.value.middle_name} ${data.value.last_name}` :  `${data.value.first_name} ${data.value.last_name}`);
      fd.append('email_applicant', data.value.email);
      fd.append('photograph_applicant', this.photo);
      fd.append('trade_licence', this.trade_licence);
      fd.append('establishment_name', data.value.establishment_name);
      fd.append('establishment_address', data.value.address);
      fd.append('establishment_pincode', '737101');
      fd.append('situation_of_other_premises', data.value.situation);
      fd.append('establishment_category', data.value.establishment_category);
      fd.append('nature_business', data.value.nature_of_business);
      fd.append('total_emplyee_male_18', data.value.total_emplyee_male_18);
      fd.append('total_emplyee_female_18', data.value.total_emplyee_female_18);
      fd.append('total_emplyee_other_18', data.value.total_emplyee_other_18);
      fd.append('total_emplyee_male_14', data.value.total_emplyee_male_14);
      fd.append('total_emplyee_female_14', data.value.total_emplyee_female_14);
      fd.append('total_emplyee_other_14', data.value.total_emplyee_other_14);
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
        },
        error: (error) => {
          console.error('Error in data:', error);
          // Display error message to the user, e.g., using a notification or alert
        }
      })
    }
  }
}
