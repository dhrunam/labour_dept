import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class ApplicationsService{
    constructor(private http: HttpClient){}

    get_applications(){
        return this.http.get<any>(`${URL}/api/application/establishment/list`);
    }
    get_application(id:number){
        return this.http.get<any>(`${URL}/api/application/establishment/${id}`);
    }
}