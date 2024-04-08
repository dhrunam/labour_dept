import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../environment/environment";

@Injectable({ providedIn: 'root' })

export class FormService{
    constructor(private http: HttpClient){}

    get_districts(){
        return this.http.get<any>(`${URL}/api/master/district`);
    }
    get_establishments(){
        return this.http.get<any>(`${URL}/api/master/establishment/category`);
    }
    get_offices(){
        return this.http.get<any>(`${URL}/api/master/office`);
    }
    submit_application(fd: FormData){
        return this.http.post<any>(`${URL}/api/application/establishment/list`, fd);
    }
}