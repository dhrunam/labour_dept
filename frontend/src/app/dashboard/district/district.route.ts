import { Routes } from "@angular/router";

export const routes: Routes = [
    { path: '', redirectTo: '/dashboard/district/view', pathMatch: 'full'},
    { path: 'view', loadComponent: () => import('./view/view.component').then(c => c.ViewComponent ) },
    { path: 'add', loadComponent: () => import('./edit/edit.component').then(c => c.EditComponent ) },
]