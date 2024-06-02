import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { UsersService } from '../users.service';

@Component({
  selector: 'app-view',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './view.component.html',
  styleUrl: './view.component.css'
})
export class ViewComponent {
  constructor(private userService: UsersService){}

  ngOnInit(): void{
    this.userService.get_registered_users().subscribe({
      next: data => {
        console.log(data);
      }
    })
  }
}
