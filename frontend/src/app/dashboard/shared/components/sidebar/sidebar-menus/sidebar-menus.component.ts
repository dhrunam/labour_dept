import { Component, Input, Renderer2 } from '@angular/core';
import { Router } from '@angular/router';
import { LocalStorageService } from '../../../../../services/local-storage.service';

@Component({
  selector: 'app-sidebar-menus',
  templateUrl: './sidebar-menus.component.html',
  styleUrl: './sidebar-menus.component.css'
})
export class SidebarMenusComponent {
  subMenuToggle: boolean = false;
  toggleKey: string = '';
  showDeptAdmin: Array<string> = ['grievance_general', 'grievance_sh', 'grievance_sh_staff', 'grievance_sh_judicial'];
  subMenuSorting!: { showSuperAdmin: boolean, showLevel1Admin: boolean, showLevel2Admin: boolean, showGeneralUser :boolean };
  @Input() toggleValue: boolean = false;
  constructor(private renderer: Renderer2, private router: Router, private localStorageService: LocalStorageService){}
  ngOnInit():void{
    this.subMenuSorting = {
      showSuperAdmin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'superadmin'),
      showLevel1Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level1_dept_admin'),
      showLevel2Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level2_dept_admin'),
      showGeneralUser: this.localStorageService.getDetails().related_group.some((i:any)=> i.name === 'general_user'),
      
    }
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
