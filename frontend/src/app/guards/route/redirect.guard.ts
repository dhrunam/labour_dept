import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { LocalStorageService } from '../../services/local-storage.service';

export const redirectGuard: CanActivateFn = (route, state) => {
  let localStorageService = inject(LocalStorageService);
  if(!localStorageService.getToken()||localStorageService.getToken()=='undefined'){
    return true;
  }
  window.location.href = '/dashboard';
  return false;
};
