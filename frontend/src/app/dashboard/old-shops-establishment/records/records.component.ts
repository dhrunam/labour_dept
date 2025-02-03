import { Component } from '@angular/core';
import { RecordsService } from './records.service';
import { RouterModule } from '@angular/router';
import { FormsModule, NgForm } from '@angular/forms';

@Component({
  selector: 'app-records',
  standalone: true,
  imports: [RouterModule, FormsModule],
  templateUrl: './records.component.html',
  styleUrl: './records.component.css'
})
export class RecordsComponent {
  applications: Array<any> = [];
  loader: boolean = false;
  constructor(private recordsService: RecordsService){}
  ngOnInit(): void{
   this.get_old_certificate_of_establishment()
  }

  onSearch(data: NgForm){
    if(!data.valid){
      data.control.markAllAsTouched();
    }
    else{
      this.loader = true;
      this.recordsService.get_applications_by_search_text(data.value.search_text).subscribe({
        next: data => {
          this.loader = false;
          this.applications=[];
          this.applications = data.results;
          console.log(data.results);
        }
      })
    }

  }

  get_old_certificate_of_establishment()
  {
    this.recordsService.get_applications().subscribe({
      next: data => {
        this.loader = false;
        this.applications=[];
        this.applications = data.results;
        console.log(data.results);
      }
    })
  }
}
