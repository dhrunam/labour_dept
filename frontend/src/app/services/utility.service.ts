import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UtilityService {

  constructor() { }


formatDate(dateString: string): string {
  const date = new Date(dateString);
  const options: Intl.DateTimeFormatOptions = {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
  };
  return date.toLocaleDateString('en-GB', options); // 'en-GB' ensures the format is dd MMM yyyy
}


convertToDatetimeLocalFormat(isoDate: string): string {
  // Create a new Date object from the ISO date string
  const date = new Date(isoDate);

  // Get the components of the date and time
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  // Format the date and time to match `datetime-local` input
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

}
