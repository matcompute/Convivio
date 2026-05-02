import { useState } from "react";

const initialForm = {
  title: "May weekday revival",
  objective: "Increase Tuesday to Thursday reservations",
  audience: "Repeat guests who have not booked in the last 30 days",
  channel_mix: ["Instagram", "Email"],
  offer: "Chef pairing on weekday reservations before 19:30",
  timing: "The next 10 days",
  notes: "Keep the voice premium and intimate. Avoid discount-heavy language.",
};

export function CampaignStudio({ campaigns, onGenerate, onApprove, loading }) {
  const [form, setForm] = useState(initialForm);

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }));
  };

  const toggleChannel = (channel) => {
    setForm((current) => {
      const exists = current.channel_mix.includes(channel);
      return {
        ...current,
        channel_mix: exists
          ? current.channel_mix.filter((item) => item !== channel)
          : [...current.channel_mix, channel],
      };
    });
  };

  const submit = (event) => {
    event.preventDefault();
    onGenerate(form);
  };

  const featured = campaigns[0];

  return (
    <section className="view-stack">
      <div className="two-column-band">
        <form className="surface dense-surface" onSubmit={submit}>
          <div className="surface-header">
            <h3>Campaign brief</h3>
            <span>Strategist input</span>
          </div>

          <label>
            Title
            <input value={form.title} onChange={(event) => updateField("title", event.target.value)} />
          </label>

          <label>
            Objective
            <input
              value={form.objective}
              onChange={(event) => updateField("objective", event.target.value)}
            />
          </label>

          <label>
            Audience
            <input
              value={form.audience}
              onChange={(event) => updateField("audience", event.target.value)}
            />
          </label>

          <label>
            Offer
            <input value={form.offer} onChange={(event) => updateField("offer", event.target.value)} />
          </label>

          <label>
            Timing
            <input value={form.timing} onChange={(event) => updateField("timing", event.target.value)} />
          </label>

          <label>
            Notes
            <textarea value={form.notes} onChange={(event) => updateField("notes", event.target.value)} />
          </label>

          <div className="channel-pills">
            {["Instagram", "Email", "WhatsApp", "SMS"].map((channel) => (
              <button
                type="button"
                key={channel}
                className={form.channel_mix.includes(channel) ? "pill active" : "pill"}
                onClick={() => toggleChannel(channel)}
              >
                {channel}
              </button>
            ))}
          </div>

          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Generating..." : "Generate campaign"}
          </button>
        </form>

        <section className="surface">
          <div className="surface-header">
            <h3>Latest generated campaign</h3>
            <span>{featured ? featured.status : "No output yet"}</span>
          </div>

          {featured ? (
            <div className="campaign-output">
              <div className="campaign-summary">
                <strong>{featured.title}</strong>
                <p>{featured.strategist_summary}</p>
                <small>Offer: {featured.suggested_offer}</small>
              </div>

              <div className="draft-list">
                {featured.channel_drafts.map((draft) => (
                  <article key={draft.channel} className="draft-card">
                    <span>{draft.channel}</span>
                    <strong>{draft.headline}</strong>
                    <p>{draft.body}</p>
                    <em>{draft.cta}</em>
                  </article>
                ))}
              </div>

              {featured.status !== "Approved" ? (
                <button className="secondary-button" type="button" onClick={() => onApprove(featured.id)}>
                  Approve latest campaign
                </button>
              ) : null}
            </div>
          ) : (
            <p className="empty-state">Generate a brief to see strategist and channel outputs here.</p>
          )}
        </section>
      </div>

      <section className="surface">
        <div className="surface-header">
          <h3>Campaign library</h3>
          <span>{campaigns.length} records</span>
        </div>
        <div className="library-grid">
          {campaigns.map((campaign) => (
            <article className="library-item" key={campaign.id}>
              <span>{campaign.status}</span>
              <strong>{campaign.title}</strong>
              <p>{campaign.objective}</p>
              <small>{new Date(campaign.created_at).toLocaleString()}</small>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
