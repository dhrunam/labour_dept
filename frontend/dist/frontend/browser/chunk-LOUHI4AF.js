import{a as k}from"./chunk-Q4HGOK7L.js";import{a as D,b as R,c as A,d as L,e as G,f as z,j as B,k as H,l as K}from"./chunk-LZEWMCEB.js";import{a as V}from"./chunk-DNLRMMXQ.js";import{b as q,i as O,m as j}from"./chunk-BH5IOZ3E.js";import{m as F,o as N}from"./chunk-MN44VEXJ.js";import{Ga as l,Ha as b,M as y,R as S,Wa as d,X as h,Ya as m,da as E,ea as M,eb as r,fb as n,gb as c,jb as I,lb as P,mb as g,rb as s,sb as a,xb as T}from"./chunk-EN6TLIPF.js";import"./chunk-CGT2X6C5.js";var U=(()=>{let t=class t{constructor(i,o){this.http=i,this.localStorageService=o}signup(i){return this.http.post(`${V}/api/user/register`,i)}};t.\u0275fac=function(o){return new(o||t)(S(q),S(k))},t.\u0275prov=y({token:t,factory:t.\u0275fac,providedIn:"root"});let e=t;return e})();function Q(e,t){e&1&&(r(0,"small",24),a(1,"Please enter first name"),n())}function W(e,t){e&1&&(r(0,"small",24),a(1,"Please enter last name"),n())}function X(e,t){e&1&&(r(0,"small",24),a(1,"Please enter email"),n())}function Y(e,t){e&1&&(r(0,"small",24),a(1,"Invalid Email (Eg. abcd@domain.com)"),n())}function Z(e,t){if(e&1&&(r(0,"div"),d(1,X,2,0,"small",15)(2,Y,2,0,"small",15),n()),e&2){g();let p=s(22);l(),m("ngIf",p.errors.required),l(),m("ngIf",p.errors.email)}}function ee(e,t){e&1&&(r(0,"small",24),a(1,"Please enter contact number"),n())}function te(e,t){e&1&&(r(0,"small",24),a(1,"Invalid Contact Number"),n())}function ne(e,t){if(e&1&&(r(0,"div"),d(1,ee,2,0,"small",15)(2,te,2,0,"small",15),n()),e&2){g();let p=s(28);l(),m("ngIf",p.errors.required),l(),m("ngIf",p.errors.email)}}function ie(e,t){e&1&&(r(0,"small",24),a(1,"Please enter password"),n())}function re(e,t){e&1&&(r(0,"small",24),a(1,"Please confirm password"),n())}function oe(e,t){e&1&&(r(0,"small",24),a(1,"Password Mismatch"),n())}function ae(e,t){if(e&1&&(r(0,"div"),d(1,re,2,0,"small",15)(2,oe,2,0,"small",15),n()),e&2){g();let p=s(34),i=s(40);l(),m("ngIf",i.invalid),l(),m("ngIf",p.value!==i.value&&!i.invalid)}}var _e=(()=>{let t=class t{constructor(i,o){this.registrationService=i,this.router=o,this.selected_gender="",this.site_key=""}onFormSubmit(i){if(!i.valid)i.control.markAllAsTouched();else{let o=new FormData;o.append("first_name",i.value.first_name),o.append("last_name",i.value.last_name),o.append("email",i.value.email),o.append("contact_number",i.value.contact),o.append("password",i.value.pswd),o.append("group","general_user"),o.append("is_deleted","False"),console.log("Password:"+o.get("password")),this.registrationService.signup(o).subscribe({next:_=>{_&&this.router.navigate(["/signup-success"])}})}}onGetIdProof(i){i.target.files&&(this.id_proof=i.target.files[0])}};t.\u0275fac=function(o){return new(o||t)(b(U),b(O))},t.\u0275cmp=h({type:t,selectors:[["app-signup"]],standalone:!0,features:[T],decls:45,vars:7,consts:[["registration","ngForm"],["first_name","ngModel"],["last_name","ngModel"],["email","ngModel"],["contact","ngModel"],["pswd","ngModel"],["pswd2","ngModel"],[1,"vh-100","d-flex","justify-content-center","align-items-center",2,"background-color","#fbfdfe"],[1,"card","w-50","p-4"],[1,"row","card-body","mb-5"],[3,"ngSubmit"],[1,"row"],[1,"col-xl-6","col-lg-12","col-md-12","mt-2"],[1,"form-label"],["type","text","name","first_name","ngModel","","required","",1,"form-control"],["class","text-danger",4,"ngIf"],["type","text","name","last_name","ngModel","","required","",1,"form-control"],["type","email","name","email","ngModel","","required","","email","",1,"form-control"],[4,"ngIf"],["type","text","name","contact","ngModel","","required","",1,"form-control"],["type","password","name","pswd","ngModel","","required","",1,"form-control"],["type","password","name","pswd2","ngModel","","required","",1,"form-control"],[1,"mt-3","mb-5","text-center"],[1,"btn","btn-primary","w-100",3,"disabled"],[1,"text-danger"]],template:function(o,_){if(o&1){let f=I();r(0,"section",7)(1,"div",8)(2,"div",9)(3,"form",10,0),P("ngSubmit",function(){E(f);let u=s(4);return M(_.onFormSubmit(u))}),r(5,"div",11)(6,"div",12)(7,"label",13),a(8,"First Name"),n(),c(9,"input",14,1),d(11,Q,2,0,"small",15),n(),r(12,"div",12)(13,"label",13),a(14,"Last Name"),n(),c(15,"input",16,2),d(17,W,2,0,"small",15),n(),r(18,"div",12)(19,"label",13),a(20,"Email"),n(),c(21,"input",17,3),d(23,Z,3,2,"div",18),n(),r(24,"div",12)(25,"label",13),a(26,"Contact"),n(),c(27,"input",19,4),d(29,ne,3,2,"div",18),n(),r(30,"div",12)(31,"label",13),a(32,"Password"),n(),c(33,"input",20,5),d(35,ie,2,0,"small",15),n(),r(36,"div",12)(37,"label",13),a(38,"Confirm Password"),n(),c(39,"input",21,6),d(41,ae,3,2,"div",18),n()(),r(42,"div",22)(43,"button",23),a(44,"Submit"),n()()()()()()}if(o&2){let f=s(10),v=s(16),u=s(22),C=s(28),x=s(34),w=s(40);l(11),m("ngIf",f.touched&&f.invalid),l(6),m("ngIf",v.touched&&v.invalid),l(6),m("ngIf",u.touched&&u.invalid),l(6),m("ngIf",C.touched&&C.invalid),l(6),m("ngIf",x.touched&&x.invalid),l(6),m("ngIf",w.touched),l(2),m("disabled",x.value!==w.value)}},dependencies:[K,z,D,R,A,B,H,G,L,j,N,F],styles:['@font-face{font-family:pt-serif;src:url("./media/ptserif-F7BF3FTK.ttf")}.card[_ngcontent-%COMP%]{box-shadow:0 7px 14px #4145581a,0 3px 6px #00000012;-webkit-box-shadow:0 7px 14px 0 rgba(65,69,88,.1),0 3px 6px 0 rgba(0,0,0,.07);-moz-box-shadow:0 7px 14px 0 rgba(65,69,88,.1),0 3px 6px 0 rgba(0,0,0,.07);border:none;border-radius:20px}.btn-primary[_ngcontent-%COMP%]{background-color:#179aff;border-color:#179aff}.tags[_ngcontent-%COMP%]{font-family:pt-serif}.heading[_ngcontent-%COMP%]{color:#606060}label[_ngcontent-%COMP%]{color:#008df9}img[_ngcontent-%COMP%]{transition:all 1s ease}img[_ngcontent-%COMP%]:hover{transform:scale(1.1)}input.ng-invalid.ng-touched[_ngcontent-%COMP%]{border-color:red}input[_ngcontent-%COMP%]{border-radius:20px;padding:.7em}']});let e=t;return e})();export{_e as SignupComponent};
