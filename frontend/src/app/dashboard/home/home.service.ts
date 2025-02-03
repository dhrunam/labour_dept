import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class HomeService{
    constructor(private http: HttpClient){}

    get_dashboard_report(){
        return this.http.get<any>(`${URL}/api/dashboard/report`);
    }
    
}