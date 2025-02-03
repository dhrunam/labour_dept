import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { URL } from "../../../../environment/environment";

@Injectable({ providedIn: 'root' })
export class RecordsService{
    constructor(private http: HttpClient){}

    get_applications(){
        return this.http.get<any>(`${URL}/api/old/establishment/list`);
    }
    get_applications_by_search_text(search_text:string){
        return this.http.get<any>(`${URL}/api/old/establishment/list?search_text=${search_text}`);
    }
    get_application(id:number){
        return this.http.get<any>(`${URL}/api/old/establishment/${id}`);
    }

    patch_application(fd:FormData){
        return this.http.patch(`${URL}/api/old/establishment/${fd.get('id')}`, fd);
    }
}