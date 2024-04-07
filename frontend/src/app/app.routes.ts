import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
    { path: 'acknowledgement', loadComponent: () => import('./acknowledgement/acknowledgement.component').then(c => c.AcknowledgementComponent ) }
];
