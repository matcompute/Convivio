export function LoginView({ form, setForm, onSubmit, error, loading }) {
  return (
    <div className="login-shell">
      <div className="login-copy">
        <span className="eyebrow">AI Go-To-Market Suite</span>
        <h1>Convivio</h1>
        <p>
          Strategy, campaign copy, review recovery, and retention playbooks for hospitality brands that
          want growth without losing their tone.
        </p>
        <div className="login-highlights">
          <article>
            <strong>Strategist agent</strong>
            <span>Shapes commercial direction before any copy is drafted.</span>
          </article>
          <article>
            <strong>Review desk</strong>
            <span>Turns guest feedback into warm, brand-safe response drafts.</span>
          </article>
          <article>
            <strong>Retention lab</strong>
            <span>Builds repeat-guest and win-back plays with clear action steps.</span>
          </article>
        </div>
      </div>

      <form className="login-panel" onSubmit={onSubmit}>
        <div className="panel-header">
          <span className="eyebrow">Workspace Access</span>
          <h2>Sign in</h2>
        </div>

        <label>
          Email
          <input
            type="email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            placeholder="owner@convivio.io"
            autoComplete="username"
          />
        </label>

        <label>
          Password
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
            placeholder="Convivio123!"
            autoComplete="current-password"
          />
        </label>

        {error ? <p className="error-banner">{error}</p> : null}

        <button type="submit" className="primary-button" disabled={loading}>
          {loading ? "Signing in..." : "Enter workspace"}
        </button>

        <div className="demo-credentials">
          <span>Demo accounts</span>
          <ul>
            <li>owner@convivio.io</li>
            <li>marketing@convivio.io</li>
            <li>ops@convivio.io</li>
          </ul>
        </div>
      </form>
    </div>
  );
}
