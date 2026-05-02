export function OverviewPanel({ dashboard, campaigns, reviews, plans }) {
  return (
    <section className="view-stack">
      <div className="hero-band">
        <div>
          <span className="eyebrow">Commercial signal</span>
          <h2>Run growth like a hospitality brand, not a spreadsheet.</h2>
        </div>
        <p>
          Convivio keeps the strategist, copy, guest recovery, and retention loops visible in one place so
          teams can move quickly without sounding generic.
        </p>
      </div>

      <div className="metric-grid">
        {dashboard.metrics.map((metric) => (
          <article className="metric-panel" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>{metric.detail}</small>
            <em>{metric.trend}</em>
          </article>
        ))}
      </div>

      <div className="two-column-band">
        <section className="surface">
          <div className="surface-header">
            <h3>Active objectives</h3>
            <span>{dashboard.active_objectives.length} priorities</span>
          </div>
          <ul className="bullet-list">
            {dashboard.active_objectives.map((objective) => (
              <li key={objective}>{objective}</li>
            ))}
          </ul>
        </section>

        <section className="surface">
          <div className="surface-header">
            <h3>Workflow snapshot</h3>
            <span>Today</span>
          </div>
          <div className="snapshot-grid">
            <article>
              <strong>{campaigns.filter((item) => item.status === "Approved").length}</strong>
              <span>Approved campaigns</span>
            </article>
            <article>
              <strong>{reviews.filter((item) => item.status !== "Closed").length}</strong>
              <span>Reviews waiting</span>
            </article>
            <article>
              <strong>{plans.length}</strong>
              <span>Retention plays</span>
            </article>
          </div>
        </section>
      </div>

      <section className="surface">
        <div className="surface-header">
          <h3>Recent highlights</h3>
          <span>Agent activity</span>
        </div>
        <div className="timeline">
          {dashboard.highlights.map((item) => (
            <article className={`timeline-item tone-${item.tone}`} key={item.id}>
              <strong>{item.title}</strong>
              <p>{item.detail}</p>
              <small>{new Date(item.timestamp).toLocaleString()}</small>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
