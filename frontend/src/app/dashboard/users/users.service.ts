import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class UsersService{
    constructor(private http: HttpClient){}
    get_registered_users(){
        return this.http.get<any>(`${URL}/api/user/list`);
    }
    register_user(fd: FormData){
        return this.http.post(`${URL}/api/admin/user/register`, fd);
    }
    
}