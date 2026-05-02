import { useState } from "react";

const initialPlan = {
  objective: "Recover weekday repeat traffic",
  at_risk_segment: "Guests who visited twice in the last 90 days but not in the last 30 days",
  incentive: "Chef pairing invitation with an early-evening welcome sip",
  horizon_days: 30,
};

export function RetentionLab({ plans, onGenerate, loading }) {
  const [form, setForm] = useState(initialPlan);

  const submit = (event) => {
    event.preventDefault();
    onGenerate({
      ...form,
      horizon_days: Number(form.horizon_days),
    });
  };

  return (
    <section className="view-stack">
      <div className="two-column-band">
        <form className="surface dense-surface" onSubmit={submit}>
          <div className="surface-header">
            <h3>Retention planner</h3>
            <span>Loyalty and win-back</span>
          </div>

          <label>
            Objective
            <input
              value={form.objective}
              onChange={(event) => setForm({ ...form, objective: event.target.value })}
            />
          </label>

          <label>
            At-risk segment
            <textarea
              value={form.at_risk_segment}
              onChange={(event) => setForm({ ...form, at_risk_segment: event.target.value })}
            />
          </label>

          <label>
            Incentive
            <input
              value={form.incentive}
              onChange={(event) => setForm({ ...form, incentive: event.target.value })}
            />
          </label>

          <label>
            Horizon days
            <input
              type="number"
              min="7"
              max="180"
              value={form.horizon_days}
              onChange={(event) => setForm({ ...form, horizon_days: event.target.value })}
            />
          </label>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Planning..." : "Generate retention plan"}
          </button>
        </form>

        <section className="surface">
          <div className="surface-header">
            <h3>Latest plan</h3>
            <span>{plans.length ? "Freshest output" : "No plan yet"}</span>
          </div>

          {plans.length ? (
            <article className="retention-plan">
              <strong>{plans[0].objective}</strong>
              <p>{plans[0].summary}</p>
              <div className="plan-steps">
                {plans[0].actions.map((action) => (
                  <div key={action.step}>
                    <span>{action.step}</span>
                    <p>{action.action}</p>
                    <small>{action.trigger}</small>
                  </div>
                ))}
              </div>
            </article>
          ) : (
            <p className="empty-state">Generate a retention plan to see structured actions here.</p>
          )}
        </section>
      </div>

      <section className="surface">
        <div className="surface-header">
          <h3>Plan history</h3>
          <span>{plans.length} playbooks</span>
        </div>
        <div className="library-grid">
          {plans.map((plan) => (
            <article className="library-item" key={plan.id}>
              <span>{plan.segment}</span>
              <strong>{plan.objective}</strong>
              <p>{plan.summary}</p>
              <small>{new Date(plan.created_at).toLocaleString()}</small>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
