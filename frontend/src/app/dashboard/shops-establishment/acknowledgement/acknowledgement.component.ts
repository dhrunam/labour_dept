import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-acknowledgement',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './acknowledgement.component.html',
  styleUrl: './acknowledgement.component.css'
})
export class AcknowledgementComponent {
  ngOnInit(): void{
    window.scrollTo(0, 0);
  }
}
