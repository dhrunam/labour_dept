import { Routes } from '@angular/router';
import { authGuard } from './guards/route/auth.guard';
import { redirectGuard } from './guards/route/redirect.guard';

export const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', loadComponent: () => import('./login/login.component').then(c => c.LoginComponent ), canActivate: [redirectGuard] },
    { path: 'dashboard', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule ), canActivate: [authGuard] },
];
