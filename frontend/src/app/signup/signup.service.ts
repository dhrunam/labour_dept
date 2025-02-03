import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../environment/environment";
import { tap } from "rxjs";
import { LocalStorageService } from "../services/local-storage.service";


@Injectable({
  providedIn: 'root'
})
export class SignupService {

  constructor(private http: HttpClient, private localStorageService: LocalStorageService){}

  signup(fd: FormData){
      return this.http.post<any>(`${URL}/api/user/register`,fd);
  }
 
}
