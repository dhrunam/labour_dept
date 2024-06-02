import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ApplicationsService } from '../applications/applications.service';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-details',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './details.component.html',
  styleUrl: './details.component.css'
})
export class DetailsComponent {
  details:any;
  constructor(private applicationService: ApplicationsService, private route: ActivatedRoute){}
  ngOnInit(): void{
    this.route.params.subscribe({
      next: (params: Params) => {
        this.getDetails(params['id']);
      }
    })
  }
  getDetails(id:number){
    this.applicationService.get_application(id).subscribe({
      next: data => {
        this.details = data;
        console.log(data);
      }
    })
  }
}
