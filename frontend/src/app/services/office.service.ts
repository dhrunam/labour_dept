import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { URL } from '../../environment/environment';
import { IOfficeDetails } from '../interfaces/ioffice-details';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OfficeService {
  constructor(private http: HttpClient){}

get_all_by_district(district_id:number): Observable<IOfficeDetails[]>{
    return this.http.get<{ results: IOfficeDetails[] }>(`${URL}/api/master/office?district=${district_id}`)
    .pipe(
        map(response=>response.results.map(item=>({
          id: item.id,
          office: item.office,
          address: item.address,
          district: item.district,
          office_type: item.office_type,
          pin: item.pin,
          is_deleted: item.is_deleted
      })))
    );
}

get_all_by_login_officer(): Observable<IOfficeDetails[]>{
  return this.http.get<{ results: IOfficeDetails[] }>(`${URL}/api/master/office`)
  .pipe(
      map(response=>response.results.map(item=>({
        id: item.id,
        office: item.office,
        address: item.address,
        district: item.district,
        office_type: item.office_type,
        pin: item.pin,
        is_deleted: item.is_deleted
    })))
  );
}

get_all(): Observable<IOfficeDetails[]>{
  return this.http.get<{ results: IOfficeDetails[] }>(`${URL}/api/master/office`)
  .pipe(
      map(response=>response.results.map(item=>({
        id: item.id,
        office: item.office,
        address: item.address,
        district: item.district,
        office_type: item.office_type,
        pin: item.pin,
        is_deleted: item.is_deleted
    })))
  );
}




get_single_by_id(id: number): Observable<IOfficeDetails> {
  // const url = `${URL}/api/master/office/${id}`;  // Adjust the URL path as per your API
  return this.http.get<IOfficeDetails>(`${URL}/api/master/office/${id}`)
      .pipe(
          map(item => ({
              id: item.id,
              address: item.address,
              district: item.district,
              office_type: item.office_type,
              pin: item.pin,
              is_deleted: item.is_deleted
             
          }))
      );
}



submit_application(fd: FormData){
    return this.http.post<any>(`${URL}/api/application/establishment/list`, fd);
}
}