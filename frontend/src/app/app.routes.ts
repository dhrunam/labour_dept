import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
    { path: 'login', loadComponent: () => import('./login/login.component').then(c => c.LoginComponent ) },
    { path: 'registration', loadComponent: () => import('./registration/registration.component').then(c => c.RegistrationComponent ) },
    { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule ) },
    { path: 'acknowledgement', loadComponent: () => import('./acknowledgement/acknowledgement.component').then(c => c.AcknowledgementComponent ) },
    { path: 'applications', loadComponent: () => import('./applications/applications.component').then(c => c.ApplicationsComponent ) },
    { path: 'details/:id', loadComponent: () => import('./details/details.component').then(c => c.DetailsComponent ) },
];
