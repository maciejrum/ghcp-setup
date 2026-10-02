import type { IncidentPage, Tenant } from './types';

export async function fetchIncidents(
  tenant: Tenant,
  page: number,
  pageSize: number,
): Promise<IncidentPage> {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
  });
  const response = await fetch(`/api/incidents?${params}`, {
    headers: { 'X-Tenant-ID': tenant },
  });

  if (!response.ok) {
    throw new Error('Unable to load incidents. Please try again.');
  }
  return response.json() as Promise<IncidentPage>;
}
