import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
const routes: Routes = [
  // { path: 'apply', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
  // { path: 'acknowledgement', loadComponent: () => import('./acknowledgement/acknowledgement.component').then(c => c.AcknowledgementComponent ) },
  { path: 'records', loadComponent: () => import('./records/records.component').then(c => c.RecordsComponent ) },

  { path: 'details/:id', loadComponent: () => import('./details/details.component').then(c => c.DetailsComponent ) },
]
@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ]
})
export class OldShopsEstablishmentModule { }
