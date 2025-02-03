
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-signup-success',
  standalone: true,
  imports: [],
  templateUrl: './signup-success.component.html',
  styleUrl: './signup-success.component.css'
})
export class SignupSuccessComponent implements OnInit {
  constructor(private router: Router) { }

  ngOnInit()
  {

  }

  redirectToLogin() {
    this.router.navigate(['/login']);
  }
}
