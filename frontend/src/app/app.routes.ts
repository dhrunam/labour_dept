import { Routes } from '@angular/router';

export const routes: Routes = [
    { path: '', loadComponent: () => import('./form/form.component').then(c => c.FormComponent ) },
];
