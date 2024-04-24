import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../environment/environment";

@Injectable({ providedIn: 'root' })
export class RegistrationService{
    constructor(private http: HttpClient){}

    register_user(fd: FormData){
        return this.http.post(`${URL}/api/user/register`, fd);
    }
}