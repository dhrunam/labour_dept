import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
const routes: Routes = [
  { path: 'apply', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
  { path: 'acknowledgement', loadComponent: () => import('./acknowledgement/acknowledgement.component').then(c => c.AcknowledgementComponent ) },
  { path: 'applications', loadComponent: () => import('./applications/applications.component').then(c => c.ApplicationsComponent ) },
  { path: 'details/:id', loadComponent: () => import('./details/details.component').then(c => c.DetailsComponent ) },
]
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ]
})
export class ShopsEstablishmentModule { }
