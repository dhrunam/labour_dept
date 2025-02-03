import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { URL } from '../../environment/environment';
import { IDistrict } from '../interfaces/idistrict';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DistrictService {
  constructor(private http: HttpClient){}
  get_districts(){
    return this.http.get<any>(`${URL}/api/master/district`);
    }
    get_all_by_district(district_id:number): Observable<IDistrict[]>{
        return this.http.get<{ results: IDistrict[] }>(`${URL}/api/master/district`)
        .pipe(
            map(response=>response.results.map(item=>({
              id: item.id,
              district_name: item.district_name,
              short_name: item.short_name,
              ref_no_prefix: item.ref_no_prefix,
              is_deleted: item.is_deleted
          })))
        );
    }
}

