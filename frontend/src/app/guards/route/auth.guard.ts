import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { LocalStorageService } from '../../services/local-storage.service';

export const authGuard: CanActivateFn = (route, state) => {
  let localStorageService = inject(LocalStorageService);
  if(localStorageService.getToken()){
    return true
  }
  alert('Please login to access dashboard');
  window.location.href = '/login';
  return false;
};
