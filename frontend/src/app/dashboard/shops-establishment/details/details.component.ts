import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { ApplicationsService } from '../applications/applications.service';
import { ActivatedRoute, Params } from '@angular/router';
import { DetailsService } from './details.service';
import { LocalStorageService } from '../../../services/local-storage.service';
import { CommonModule } from '@angular/common';
import { Print } from '../../shared/methods/print';

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './details.component.html',
  styleUrl: './details.component.css'
})
export class DetailsComponent {
  @ViewChild('closeBtn', { static: true } ) private closeBtn!: ElementRef;
  form_id:number = 0;
  showLoader: boolean = false;
  details:any;
  displayStatus: string = '';
  status: string = '';
  print = new Print();
  role!: { showLevel1Admin: boolean, showLevel2Admin: boolean, showLevel3Admin: boolean }
  constructor(private applicationService: ApplicationsService, private route: ActivatedRoute, private detailService: DetailsService, private localStorageService: LocalStorageService){
    this.role = {
      showLevel1Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level1_dept_admin'),
      showLevel2Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level2_dept_admin'),
      showLevel3Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level3_dept_admin'),
    }
  }
  ngOnInit(): void{
    this.route.params.subscribe({
      next: (params: Params) => {
        this.getDetails(params['id']);
        this.form_id = params['id'];
      }
    })
  }
  print_certificate(){
    this.print.generatePendingReceipt(this.details);
  }
  getDetails(id:number){
    this.applicationService.get_application(id).subscribe({
      next: data => {
        this.details = data;
      }
    })
  }
  fetch_status(status: string){
    this.status = status;
    this.displayStatus = status === 'approved' ? 'approve' : 'reject';
  }
  verify_t2_application(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.showLoader = true;
      let fd = new FormData();
      fd.append('id', this.form_id.toString());
      fd.append('calculated_fee', data.value.cost);
      fd.append('application_status', 'T3-Verification')
      this.detailService.verify_t2(fd).subscribe({
        next: data => {
          this.showLoader = false;
          this.getDetails(this.form_id);
        }
      })
    }
  }
  verify_t1_application(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.showLoader = true;
      let fd = new FormData();
      fd.append('id', this.form_id.toString());
      fd.append('token_number', data.value.br);
      this.detailService.verify_t2(fd).subscribe({
        next: data => {
          this.showLoader = false;
          this.getDetails(this.form_id);
        }
      })
    }
  }
  verify_t3_application(){
    this.showLoader = true;
    let fd = new FormData();
    fd.append('id', this.form_id.toString());
    fd.append('application_status', this.status);
    this.detailService.verify_t2(fd).subscribe({
      next: data => {
        this.showLoader = false;
        this.getDetails(this.form_id);
        this.closeBtn.nativeElement.click();
      }
    })
  }
}
