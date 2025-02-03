import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule, NgForm,  } from '@angular/forms';
import { RecordsService } from '../records/records.service';
import { ActivatedRoute, Params } from '@angular/router';
import { LocalStorageService } from '../../../services/local-storage.service';
import { CommonModule } from '@angular/common';
import { Print } from '../../shared/methods/print';
import { ToastrService } from 'ngx-toastr';
import { OfficeService } from '../../../services/office.service';
import { DistrictService } from '../../district/district.service';
import { DetailsService } from './details.service';

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './details.component.html',
  styleUrl: './details.component.css'
})
export class DetailsComponent {
  @ViewChild('closeBtn', { static: true } ) private closeBtn!: ElementRef;
  details:any;
  showLoader: boolean = false;
  instance_id: number = 0;
  trade_licence: any;
  offices : Array<any> = [];
  districts: Array<any> = [];
  status: string = '';
  displayStatus: string = '';
  role!: {showGeneralUser:boolean, showLevel1Admin: boolean, showLevel2Admin: boolean }
  constructor(private print: Print,
    private recordService: RecordsService, 
    private route: ActivatedRoute, 
    private localStorageService: LocalStorageService,
    private toastr: ToastrService,
    private officeService :OfficeService,
    private districtService : DistrictService,
    private detailService : DetailsService
    ){
    this.role = {
      showGeneralUser: this.localStorageService.getDetails().related_group.some((i:any)=> i.name === 'general_user'),
      showLevel1Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level1_dept_admin'),
      showLevel2Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level2_dept_admin'),
     
    }
  }

  ngOnInit(): void{
    this.route.params.subscribe({
      next: (params: Params) => {
        this.getDetails(params['id']);
        this.instance_id = params['id'];
        console.log('showLevel2Admin:')
        console.log(this.role.showLevel2Admin)
      }
    })
    this.get_districts();
  }
  getDetails(id:number){
    this.recordService.get_application(id).subscribe({
      next: data => {
        this.details = data;
      }
    })
  }

  upload_old_registration_certificate(data: NgForm){
      this.status='received'
      if(!data.valid){
        data.control.markAllAsTouched();
      }
      else{
        this.showLoader = true;
        let fd = new FormData();
        fd.append('id', this.instance_id.toString());
        fd.append('registration_certificate', this.trade_licence);
        fd.append('district', data.value.district);
        fd.append('applied_office_details', data.value.office);
        fd.append('application_status', this.status);

        this.recordService.patch_application(fd).subscribe({
        next: data => {
          this.details = data;
        }
      })
    }

  }
  tradeLicenceUpload(event: any){
    if(event.target.files){
      this.trade_licence = event.target.files[0];
    }
  }

  get_offices(district:number){
    this.officeService.get_all_by_district(district).subscribe({
      next: data => {
        this.offices = data;
      }
    })
  }
  onDistrictChange(event:any)
  {
    const district_id=event.target.value;
    this.get_offices(district_id);
  }

  get_districts(){
    this.districtService.get_districts().subscribe({
      next: data => {
        this.districts = data.results;
      }
    })
  }

  fetch_status(status: string){
    this.status = status;
    this.displayStatus = status === 'approved' ? 'approve' : 'reject';
  }

  verify_t2_application(data: NgForm){
    this.showLoader = true;
    let fd = new FormData();
    fd.append('id', this.instance_id.toString());
    fd.append('application_status', this.status);
    fd.append('remarks', data.value.remarks);
    console.log("Remarks:")
    console.log(data.value.remarks)

    this.recordService.patch_application(fd).subscribe({
      next: data => {
        this.details = data;
        this.showLoader = false;
        this.getDetails(this.instance_id);
        this.closeBtn.nativeElement.click();
        this.toastr.success('Success!', 'Data submitted sucessfully..!');
      }
      ,
      error: (error:any)=>{
        this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
      }
    })
    
  }
}
