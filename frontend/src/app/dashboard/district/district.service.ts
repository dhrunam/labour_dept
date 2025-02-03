import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class DistrictService{
    constructor(private http: HttpClient){}
    get_districts(){
        return this.http.get<any>(`${URL}/api/master/district`);
    }
    save_district(fd: FormData){
        return this.http.post(`${URL}/api/master/district`, fd);
    }
}

