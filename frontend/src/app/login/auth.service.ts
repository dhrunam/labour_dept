import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../environment/environment";
import { tap } from "rxjs";
import { LocalStorageService } from "../../services/local-storage.service";

@Injectable({ providedIn: 'root' })
export class AuthService{
    constructor(private http: HttpClient, private localStorageService: LocalStorageService){}

    login(fd: FormData){
        return this.http.post<any>(`${URL}/api/auth/login/`,fd).pipe(tap((respData) => this.localStorageService.saveData(respData)));
    }
    logout(){
        return this.http.post<any>(`${URL}/api/auth/logout/`, {});
    }
}