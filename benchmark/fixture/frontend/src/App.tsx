import { useEffect, useState } from 'react';
import { fetchIncidents } from './api';
import type { IncidentPage, IncidentStatus, Tenant } from './types';

const STATUS_LABELS: Record<IncidentStatus, string> = {
  open: 'Open',
  in_progress: 'In progress',
  closed: 'Closed',
};

function readPagination() {
  const params = new URLSearchParams(window.location.search);
  const page = Number(params.get('page') ?? 1);
  const pageSize = Number(params.get('page_size') ?? 5);
  return {
    page: Number.isInteger(page) && page > 0 ? page : 1,
    pageSize: Number.isInteger(pageSize) && pageSize > 0 && pageSize <= 50 ? pageSize : 5,
  };
}

export default function App() {
  const [tenant, setTenant] = useState<Tenant>('alpha');
  const [{ page, pageSize }, setPagination] = useState(readPagination);
  const [data, setData] = useState<IncidentPage | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    const syncWithLocation = () => setPagination(readPagination());
    window.addEventListener('popstate', syncWithLocation);
    return () => window.removeEventListener('popstate', syncWithLocation);
  }, []);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchIncidents(tenant, page, pageSize)
      .then(setData)
      .catch((reason: unknown) => {
        setError(reason instanceof Error ? reason.message : 'Unable to load incidents. Please try again.');
      })
      .finally(() => setLoading(false));
  }, [tenant, page, pageSize, retry]);

  function goToPage(nextPage: number) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', String(nextPage));
    window.history.pushState({}, '', url);
    setPagination({ page: nextPage, pageSize });
  }

  const totalPages = Math.max(1, Math.ceil((data?.total ?? 0) / pageSize));

  return (
    <main className="desk">
      <header className="hero">
        <div>
          <p className="eyebrow"><span className="live-dot" /> OPERATIONS / INCIDENTS</p>
          <h1>Incident Desk<span className="title-dot">.</span></h1>
          <p className="intro">One place to see what needs your team’s attention.</p>
        </div>
        <div className="workspace-control">
          <label htmlFor="tenant">Workspace</label>
          <select
            id="tenant"
            value={tenant}
            onChange={(event) => {
              setTenant(event.target.value as Tenant);
              goToPage(1);
            }}
          >
            <option value="alpha">Alpha</option>
            <option value="beta">Beta</option>
          </select>
        </div>
      </header>

      <section className="incident-panel" aria-labelledby="incident-heading">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">WORKSPACE {tenant.toUpperCase()}</p>
            <h2 id="incident-heading">Incidents</h2>
          </div>
          <span className="total-pill">{loading ? '…' : (data?.total ?? 0)} incidents</span>
        </div>

        {loading ? (
          <div className="state-message" role="status">Loading incidents…</div>
        ) : error ? (
          <div className="state-message error-state" role="alert">
            <p>{error}</p>
            <button onClick={() => setRetry((value) => value + 1)}>Retry</button>
          </div>
        ) : data?.items.length === 0 ? (
          <div className="state-message" role="status">No incidents found.</div>
        ) : (
          <div className="table-scroll">
            <table aria-label="Incidents">
              <thead>
                <tr><th scope="col">Incident</th><th scope="col">Status</th><th scope="col">Severity</th><th scope="col">Created</th></tr>
              </thead>
              <tbody>
                {data?.items.map((incident) => (
                  <tr key={incident.id}>
                    <td><span className="incident-id">{incident.id}</span><span className="incident-title">{incident.title}</span></td>
                    <td><span className={`status-badge status-${incident.status}`}>{STATUS_LABELS[incident.status]}</span></td>
                    <td><span className={`severity severity-${incident.severity}`}>{incident.severity}</span></td>
                    <td><time dateTime={incident.created_at}>{new Date(incident.created_at).toLocaleString('en-GB', { timeZone: 'UTC', dateStyle: 'medium', timeStyle: 'short' })} UTC</time></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <nav className="pagination" aria-label="Pagination">
          <span>Page {page} of {totalPages}</span>
          <div>
            <button disabled={loading || page <= 1} onClick={() => goToPage(page - 1)}>Previous</button>
            <button disabled={loading || !!error || page >= totalPages} onClick={() => goToPage(page + 1)}>Next</button>
          </div>
        </nav>
      </section>
      <footer className="desk-footer">Incident Desk <span>All times in UTC</span></footer>
    </main>
  );
}
