import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', loadComponent: () => import('./login/login.component').then(c => c.LoginComponent ) },
    { path: 'registration', loadComponent: () => import('./registration/registration.component').then(c => c.RegistrationComponent ) },
    { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule ) },
];
