import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { RenewApplicationsComponent } from './renew-applications/renew-applications.component';
const routes: Routes = [
  { path: 'apply', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
  { path: 'acknowledgement', loadComponent: () => import('./acknowledgement/acknowledgement.component').then(c => c.AcknowledgementComponent ) },
  { path: 'applications', loadComponent: () => import('./applications/applications.component').then(c => c.ApplicationsComponent ) },
  { path: 'details/:id', loadComponent: () => import('./details/details.component').then(c => c.DetailsComponent ) },
  { path: 'establishment/renew', loadComponent: () => import('./renew-applications/renew-applications.component').then(c => c.RenewApplicationsComponent ) },
  { path: 'payment/success', loadComponent: () => import('./payment-success/payment-success.component').then(c => c.PaymentSuccessComponent ) },
  { path: 'payment/fail', loadComponent: () => import('./payment-failure/payment-failure.component').then(c => c.PaymentFailureComponent ) }

]
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ]
})
export class ShopsEstablishmentModule { }
