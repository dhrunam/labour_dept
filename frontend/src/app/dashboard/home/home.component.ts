import { Component } from '@angular/core';
import { HomeService } from './home.service';
import { RouterModule } from '@angular/router';
import { FormsModule, NgForm,  } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { LocalStorageService } from '../../services/local-storage.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterModule, FormsModule,CommonModule ],
  providers: [
    HomeService // Provide the service here
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  report_data: any;
  loader: boolean = false;
  role!: {showGeneralUser:boolean, showLevel1Admin: boolean, showLevel2Admin: boolean }
  constructor(private homeService: HomeService,
   private localStorageService: LocalStorageService
  ){

    this.role = {
      showGeneralUser: this.localStorageService.getDetails().related_group.some((i:any)=> i.name === 'general_user'),
      showLevel1Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level1_dept_admin'),
      showLevel2Admin: this.localStorageService.getDetails().related_group.some((i:any) => i.name === 'level2_dept_admin'),
     
    }
  }
  ngOnInit(): void{
    this.homeService.get_dashboard_report().subscribe({
      next: data => {
        this.loader = false;
        this.report_data = data;
        console.log(data);
      }
    })
  }

}
