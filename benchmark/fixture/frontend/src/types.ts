export type Tenant = 'alpha' | 'beta';
export type IncidentStatus = 'open' | 'in_progress' | 'closed';

export interface Incident {
  id: string;
  title: string;
  status: IncidentStatus;
  severity: 'low' | 'medium' | 'high';
  created_at: string;
}

export interface IncidentPage {
  items: Incident[];
  total: number;
  page: number;
  page_size: number;
}
