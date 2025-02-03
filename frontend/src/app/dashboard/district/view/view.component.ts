import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { DistrictService } from '../district.service';

@Component({
  selector: 'app-view',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './view.component.html',
  styleUrl: './view.component.css'
})
export class ViewComponent {
  districts: Array<any> = [];
  constructor(private districtService: DistrictService){}
  ngOnInit(): void{
    this.districtService.get_districts().subscribe({
      next: data => {
        this.districts = data.results;
      }
    })
  }
}
