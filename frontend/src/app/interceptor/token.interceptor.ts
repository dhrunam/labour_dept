import { HttpHeaders, HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { LocalStorageService } from '../services/local-storage.service';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  
  let authReq = req;
  let localStorageService = inject(LocalStorageService);
  const router = inject(Router);
  const token = localStorageService.getToken();
  authReq = req.clone({headers: new HttpHeaders()});
  if(token != null){
    authReq = req.clone({headers: new HttpHeaders().set('Authorization', `Token ${token}`) } );
   }
  // return next(authReq);
  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Clear local storage on 401 unauthorized error
        localStorageService.clearSession();
        // Redirect to login page
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
  
};
