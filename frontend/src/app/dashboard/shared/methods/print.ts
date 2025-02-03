import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
pdfMake.vfs = pdfFonts.pdfMake.vfs;
import { getBase64ImageFromURL } from "./base-64.url";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class Print{
    async generatePendingReceipt(details: any){ 
        let date = new Date();
        let docDefinition:any = {  
          content: [
            {
              // image: await getBase64ImageFromURL("../../../../assets/images/seal.png" ),
              image: await getBase64ImageFromURL("../../../../assets/images/seal.png" ),
              fit: [100, 100],
              alignment: 'center',
            },
            {
              text: 'LABOUR DEPARTMENT',
              fontSize: 12,
              margin: [0, 10, 0, 0],
              alignment: 'center',
            },
            {
                text: 'GOVERNMENT OF SIKKIM',
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'center',
              },
              {
                text: 'REGISTRATION CERTIFICATE OF ESTABLISHMENT',
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'center',
              },
              {
                text: '(The Sikkim Shops and Commercial Establishment Act, 1983)',
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'center',
              },
              {
                // image: await getBase64ImageFromURL("../../../../assets/images/user.png" ),
                image: await getBase64ImageFromURL( details.photograph_applicant ),
                // text:"Paste Applicant",
                fit: [80, 80],
                margin: [0, 20, 0, 0],
                alignment: 'right',
              },
              // {
              //   // image: await getBase64ImageFromURL("../../../../assets/images/user.png" ),
              //   image: await getBase64ImageFromURL( details.photograph_applicant ),
              //   // text:"Photo here",
              //   fit: [80, 80],
              //   margin: [0, 20, 0, 0],
              //   alignment: 'right',
              // },
              {
                text: [{text: '1. Registration Mark Number: ', bold: true },`${details && details.application_no.replaceAll('-','/')}`],
                fontSize: 12,
                margin: [0, 30, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: '2. Name of the Establishment: ', bold: true },`${details && details.establishment_name}`],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: '3. Full Postal Address: ', bold: true },`${details && details.establishment_address}`],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: '4. Nature of business, trade profession carried : ', bold: true },`${details && details.nature_business}`],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: 
                  '5. Name and designation of the Proprietor/Manager/Agent or any other person in the immediate charger control of the Establishment: ', bold: true } , 
                  details.related_management_level_employee_details && 
                  details.related_management_level_employee_details.length > 0 ? 
                  details.related_management_level_employee_details[0].name + ', Age:' + details.related_management_level_employee_details[0].age: 'N/A'],
                  fontSize: 12,
                  margin: [0, 10, 0, 0],
                  alignment: 'left',
              },
              {
                text: [{text: '6. Name and designation of other person(s) having interest as Employer in the establishment in any, with his/their address in the State: ', bold: true } , 
                  details.related_employer_parentage_details &&  details.related_employer_parentage_details.length > 0 ?
                  details.related_employer_parentage_details[0].parentage_name : 'N/A'
                 
                ],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: '7. Total number of employees (Adults): ', bold: true },`${details && (details.total_emplyee_male_18+details.total_emplyee_female_18+details.total_emplyee_other_18)}`],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: [{text: '8. Total number of employees (Young): ', bold: true },`${details && (details.total_emplyee_male_14+details.total_emplyee_female_14+details.total_emplyee_other_14)}`],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },
              {
                text: `This is to certify that the Establishment, the particulars of which have been given above, has been registered under the Sikkim Shops and Commercial Establishment Act, 1983 on the day of ${date.getDate() < 10 ? '0':''}${date.getDate()}-${date.getMonth() < 10 ? '0':''}${date.getMonth()}-${date.getFullYear()}. `,
                fontSize: 12,
                margin: [0, 30, 0, 0],
                alignment: 'justified',
              },

              {
                text: [{text: 'Valid up to: 31 March, ', bold: true },
                  {text:`${date.getDate() <=3 ? date.getFullYear(): (date.getFullYear()+1)}`, bold: true}],
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'left',
              },

              {
                text: 'Chief Inspector',
                fontSize: 12,
                margin: [0, 60, 0, 0],
                alignment: 'right',
              },
              {
                text: 'Under the Sikkim Shops and',
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'right',
              },
              {
                text: 'Commercial Establishment Act, 1983',
                fontSize: 12,
                margin: [0, 10, 0, 0],
                alignment: 'right',
              },
          ]  
        };  
        pdfMake.createPdf(docDefinition).open();
    }
}