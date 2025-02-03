export class IDistrict {
    id?: number; // Optional ID field
    district_name?:string|null;
    short_name?: number | null; // Foreign key to District model
    ref_no_prefix?: number | null; // Foreign key to OfficeType model
    is_deleted?: boolean;
}
