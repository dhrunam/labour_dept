import { Component } from "@angular/core";
@Component({
    selector: 'app-dashboard',
    template: `
        <div class="d-flex">
            <app-sidebar></app-sidebar>
            <div class="d-block w-100">
                <app-header></app-header>
                <router-outlet></router-outlet>
            </div>
        </div>
    `,
})
export class DashboardComponent{}