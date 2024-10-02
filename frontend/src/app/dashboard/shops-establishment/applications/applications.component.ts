import { Component } from '@angular/core';
import { ApplicationsService } from './applications.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-applications',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './applications.component.html',
  styleUrl: './applications.component.css'
})
export class ApplicationsComponent {
  applications: Array<any> = [];
  constructor(private applicationService: ApplicationsService){}
  ngOnInit(): void{
    this.applicationService.get_applications().subscribe({
      next: data => {
        this.applications = data.results;
        console.log(data.results);
      }
    })
  }
}
