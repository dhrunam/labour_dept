import { Component, ElementRef, ViewChild, Renderer2 } from '@angular/core';
import { FormsModule, NgForm,  } from '@angular/forms';
import { ApplicationsService } from '../applications/applications.service';
import { ActivatedRoute, Params } from '@angular/router';
import { DetailsService } from './details.service';
import { LocalStorageService } from '../../../services/local-storage.service';
import { CommonModule } from '@angular/common';
import { Print } from '../../shared/methods/print';
import { ToastrService } from 'ngx-toastr';
declare var loadBillDeskSdk: any;
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

  browser_tz: string='';
  browser_color_depth: number=0;
  browser_java_enabled: boolean = false;
  browser_screen_height: number = screen.height;
  browser_screen_width: number = screen.width;
  browser_language: string | undefined = navigator.language;
  browser_javascript_enabled: boolean = true; // Always true in the browser context
 
  // print = new Print();
  role!: {showGeneralUser:boolean, showLevel1Admin: boolean, showLevel2Admin: boolean }
  constructor(private print: Print,
    private applicationService: ApplicationsService, 
    private route: ActivatedRoute, 
    private detailService: DetailsService,
    private localStorageService: LocalStorageService,
    private toastr: ToastrService,
    private renderer :Renderer2
    ){
    this.role = {
      showGeneralUser: this.localStorageService.getDetails().related_group.some((i:any)=> i.name === 'general_user'),
      showLevel1Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level1_dept_admin'),
      showLevel2Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level2_dept_admin'),
     
    }
  }
  ngOnInit(): void{
    try {
      this.browser_tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      this.browser_color_depth= screen.colorDepth
    } catch (error) {
      console.error("Could not determine timezone:", error);
      this.browser_tz = 'Unknown'; // Handle cases where timezone is not available
    }
    this.route.params.subscribe({
      next: (params: Params) => {
        this.getDetails(params['id']);
        this.form_id = params['id'];
        console.log('showLevel2Admin:')
        console.log(this.role.showLevel2Admin)

        console.log('general_user:')
        console.log(this.role.showGeneralUser)
      }
    })
    // this.loadBillDeskSDK();
  }
  print_certificate(){
    console.log(this.details)
    this.print.generatePendingReceipt(this.details);
  }
  getDetails(id:number){
    this.applicationService.get_application(id).subscribe({
      next: data => {
        this.details = data;
        console.log('Applicaqtion Details..')
        console.log(this.details)
        console.log('Applicaqtion Status..')
        console.log(this.details.application_status)
      }
    })
  }
  fetch_status(status: string){
    this.status = status;
    this.displayStatus = status === 'approved' ? 'approve' : 'reject';
  }
  verify_t1_application(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.showLoader = true;
      let fd = new FormData();
      fd.append('id', this.form_id.toString());
      fd.append('calculated_fee', data.value.cost);
      fd.append('application_status', 'T1-Verification');
      fd.append('remarks', data.value.remarks)
      this.detailService.verify_t1(fd).subscribe({
        next: data => {
         
          this.showLoader = false;
          this.getDetails(this.form_id);
          this.toastr.success('Success!', 'Data submitted sucessfully..!');

        },
        error: (error:any)=>{
          this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
        }
      })
    }
  }
  pay_application_fees(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.showLoader = true;
      let fd = new FormData();
      fd.append('application', this.form_id.toString());
      fd.append('application_no', data.value.application_no);
      fd.append('application_generation', "NEW");
      // fd.append('token_number', data.value.br);
      fd.append('amount', this.details.calculated_fee);
      // fd.append('browser_color_depth', this.browser_color_depth.toString());
      // fd.append('browser_screen_width', this.details.browser_screen_width);
      // fd.append('browser_language', this.details.browser_language);
      // fd.append('browser_java_enabled', 'false');
      // fd.append('browser_javascript_enabled', 'true');
      // fd.append('browser_tz', this.browser_tz);
      

      // fd.append('application_status', 'fee_payment_success');
      
      // this.detailService.verify_t2(fd).subscribe({
      //   next:(data:any) => {
      //     console.log("Payment message:")
      //     console.log(data)
      //     this.showLoader = false;
      //     this.getDetails(this.form_id);
      //     this.toastr.success('Success!', 'Data submitted sucessfully..!');
          
      //   },
      //   error: (error:any)=>{
      //     this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
      //   }
      // });

      this.detailService.initiate_online_payment(fd).subscribe({
        next:(data:any) => {
          console.log("Payment message:")
          console.log(data)
          this.showLoader = false;
          // // this.invokeBillDeskSDK(data.decoded_response);
          // this.getDetails(this.form_id);
          // // window.location.href = data.next_step_url;
          // this.toastr.success('Success!', 'Data submitted sucessfully..!');
                // Create a hidden form dynamically
          const form = document.createElement('form');
          form.method = 'POST';
          form.action = data.url;

          const hiddenField = document.createElement('input');
          hiddenField.type = 'hidden';
          hiddenField.name = 'msg';
          hiddenField.value = data.msg;

          form.appendChild(hiddenField);
          document.body.appendChild(form);
          form.submit();  // Automatically submits the form

              
            },
            error: (error:any)=>{
              this.showLoader = false;
              // this.getDetails(this.form_id);
              this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
            }
      });
    }
  }

  reject_at_level1(data:NgForm){
    this.showLoader = true;
    let fd = new FormData();
    fd.append('id', this.form_id.toString());
    fd.append('application_status', this.status);
    fd.append('remarks', data.value.remarks);
    console.log("Remarks:")
    console.log(data.value.remarks)
    this.detailService.reject_by_level1(fd).subscribe({
      next: data => {
       
        this.showLoader = false;
        this.getDetails(this.form_id);
        this.closeBtn.nativeElement.click();
        this.toastr.success('Success!', 'Data submitted sucessfully..!');
      }
      ,
      error: (error:any)=>{
        this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
      }
    })
  }

  verify_t2_application(data: NgForm){
    this.showLoader = true;
    let fd = new FormData();
    fd.append('id', this.form_id.toString());
    fd.append('application_status', this.status);
    fd.append('remarks', data.value.remarks);
    console.log("Remarks:")
    console.log(data.value.remarks)
    this.detailService.verify_t2(fd).subscribe({
      next: data => {
       
        this.showLoader = false;
        this.getDetails(this.form_id);
        this.closeBtn.nativeElement.click();
        this.toastr.success('Success!', 'Data submitted sucessfully..!');
      }
      ,
      error: (error:any)=>{
        this.toastr.error('Sorry!', 'Something went wrong. Please try again..!');
      }
    })
  }

  loadBillDeskSDK(): void {
    const script = this.renderer.createElement('script');
    // script.type = 'module';
    script.src = 'https://uat.billdesk.com/jssdk/v1/dist/billdesksdk.js';
    script.onload = () => console.log('BillDesk SDK Loaded');
    document.head.appendChild(script);
  }

  invokeBillDeskSDK(data:any): void {

    var flow_config = { 
      merchantId: data.mercid, 
      bdOrderId: data.bdorderid,
      authToken: data.links[1].headers.authorization,
      childWindow: false ,
      returnUrl: data.ru, 
      retryCount: 3
      // prefs: {
      // "payment_categories": ["card", "nb"], 
      // "allowed_bins": ["459150", "525211"]
      // },
      // netBanking:{ "showPopularBanks" : "Y",
      // "popularBanks": ["Kotak Bank"," AXIS Bank [Retail]"]
      // }
      }
    
    var theme_config = {
        sdkPrimaryColor: "#69068a", 
        sdkAccentColor: "#cf5df5", 
        sdkBackgroundColor: "#f2caff", 
        sdkBannerColor: "#982cbb"
        }
    
    var config = {
          // responseHandler: responseHandler,
          // merchantLogo: "data:image/png;base64:eqwewqesddhgjdxsc==" 
          flowConfig: flow_config,
          flowType: "payments", 
          
          themeConfig: theme_config
        
        }
    console.log('Launching BillDesk Payment SDK', config);
      if (typeof loadBillDeskSdk !== 'undefined') {
          loadBillDeskSdk(config);
        } else {
          console.error('BillDesk SDK not loaded properly.');
        }

  }
}
