import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class DetailsService{
    constructor(private http: HttpClient){}

    verify_t2(fd: FormData){
        return this.http.patch(`${URL}/api/application/establishment/${fd.get('id')}`, fd);
    }

    verify_t1(fd: FormData){
        return this.http.patch(`${URL}/api/application/establishment/${fd.get('id')}`, fd);
    }

    initiate_online_payment(fd: FormData){
        return this.http.post(`${URL}/api/application/online_payment/initiate`, fd);
    }

    reject_by_level1(fd: FormData){
        return this.http.patch(`${URL}/api/application/establishment/${fd.get('id')}`, fd);
    }
}