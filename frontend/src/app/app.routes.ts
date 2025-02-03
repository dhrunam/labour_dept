import { Routes } from '@angular/router';
import { authGuard } from './guards/route/auth.guard';
import { redirectGuard } from './guards/route/redirect.guard';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', loadComponent: () => import('./login/login.component').then(c => c.LoginComponent ), canActivate: [redirectGuard] },
    { path: 'signup', loadComponent: () => import('./signup/signup.component').then(c => c.SignupComponent ), canActivate: [redirectGuard] },
    { path: 'signup-success', loadComponent: () => import('./signup-success/signup-success.component').then(c => c.SignupSuccessComponent ) },
    { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule ), canActivate: [authGuard] },
];
