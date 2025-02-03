export class IOfficeDetails {
    id?: number; // Optional ID field
    office?:string|null;
    district?: number | null; // Foreign key to District model
    office_type?: number | null; // Foreign key to OfficeType model
    address?: string | null;
    pin?: string | null;
    is_deleted?: boolean;
}
