import { HttpHeaders, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { LocalStorageService } from '../services/local-storage.service';

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  let authReq = req;
  let localStorageService = inject(LocalStorageService);
  const token = localStorageService.getToken();
  console.log(token);
  authReq = req.clone({headers: new HttpHeaders()});
  if(token != null){
    authReq = req.clone({headers: new HttpHeaders().set('Authorization', `Token ${token}`) } );
   }
  return next(authReq);
};
