import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard.component';
import { HeaderComponent } from './shared/components/header/header.component';
import { SidebarComponent } from './shared/components/sidebar/sidebar.component';
import { SidebarMenusComponent } from './shared/components/sidebar/sidebar-menus/sidebar-menus.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard/home', pathMatch: 'full'},
  { path: '', component: DashboardComponent,
    children: [
      { path: 'home', loadComponent: () => import('./home/home.component').then(c => c.HomeComponent ) },
      { path: 'users', loadChildren: () => import('./users/users.route').then(r => r.routes ) },
      { path: 'shops-establishment', loadChildren: () => import('./shops-establishment/shops-establishment.module').then(m => m.ShopsEstablishmentModule ) },
    ]
  }
];
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ],
  declarations: [
    HeaderComponent,
    SidebarComponent,
    SidebarMenusComponent,
    DashboardComponent
  ]
})
export class DashboardModule { }
