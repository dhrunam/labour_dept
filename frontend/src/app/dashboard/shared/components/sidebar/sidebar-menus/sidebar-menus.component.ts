import { Component, Input, Renderer2 } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar-menus',
  templateUrl: './sidebar-menus.component.html',
  styleUrl: './sidebar-menus.component.css'
})
export class SidebarMenusComponent {
  subMenuToggle: boolean = false;
  toggleKey: string = '';
  grievances: Array<string> = ['grievance_general', 'grievance_sh', 'grievance_sh_staff', 'grievance_sh_judicial'];
  subMenuSorting!: { showGrievancesAdmin: boolean, showRTIAdmin: boolean, showGeneralUser: boolean, showMasterAdmin: boolean, showAppellateAutority: boolean, showDCJJB: boolean, showHCJJB: boolean, showCCAdmin: boolean, showAdvocate: boolean, showPaperlessAdmin: boolean };
  @Input() toggleValue: boolean = false;
  constructor(private renderer: Renderer2, private router: Router){}
  ngOnInit():void{
    // this.subMenuSorting = {
    //   showGrievancesAdmin: this.localStorageService.getDetails().related_group.some((i:any) => this.grievances.includes(i.name)),
    //   showRTIAdmin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'rti_admin'),
    //   showGeneralUser: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'general_user'),
    //   showMasterAdmin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'superadmin'),
    //   showAppellateAutority: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'appellate_authority'),
    //   showDCJJB: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'dc_jjb'),
    //   showHCJJB: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'hc_jjb'),
    //   showCCAdmin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'cc_admin'),
    //   showAdvocate: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'advocate'),
    //   showPaperlessAdmin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'paperless_admin'),
    // }
    this.toggleKey = this.router.url.split('/')[2];
    this.subMenuToggle = this.toggleKey === 'home' ? false : true;
  }
  onToggle(elem1:any, elem2: any, key:string){
    if(this.toggleKey != key){
      this.toggleKey = key;
      this.subMenuToggle = false;
    }
    this.subMenuToggle = !this.subMenuToggle
    if(this.subMenuToggle){
      this.renderer.addClass(elem1, 'open');
      this.renderer.addClass(elem2, 'active');
    }
    else{
      this.renderer.removeClass(elem1, 'open');
      this.renderer.removeClass(elem2, 'active');
    }
  }
  onToggleKey(key:string){
    this.toggleKey = key;
  }
}
