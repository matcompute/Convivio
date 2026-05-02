import { useEffect, useState } from "react";

export function ProfilePanel({ profile, onSave, loading }) {
  const [draft, setDraft] = useState(profile);

  useEffect(() => {
    setDraft(profile);
  }, [profile]);

  if (!draft) {
    return null;
  }

  const updateChannel = (index, field, value) => {
    const nextChannels = draft.channels.map((item, channelIndex) =>
      channelIndex === index ? { ...item, [field]: value } : item,
    );
    setDraft({ ...draft, channels: nextChannels });
  };

  const submit = (event) => {
    event.preventDefault();
    onSave(draft);
  };

  return (
    <section className="view-stack">
      <form className="surface dense-surface" onSubmit={submit}>
        <div className="surface-header">
          <h3>Restaurant profile</h3>
          <span>Brand grounding</span>
        </div>

        <div className="profile-grid">
          <label>
            Name
            <input value={draft.name} onChange={(event) => setDraft({ ...draft, name: event.target.value })} />
          </label>

          <label>
            City
            <input value={draft.city} onChange={(event) => setDraft({ ...draft, city: event.target.value })} />
          </label>

          <label>
            Cuisine
            <input
              value={draft.cuisine}
              onChange={(event) => setDraft({ ...draft, cuisine: event.target.value })}
            />
          </label>

          <label>
            Hero offer
            <input
              value={draft.hero_offer}
              onChange={(event) => setDraft({ ...draft, hero_offer: event.target.value })}
            />
          </label>

          <label className="full-span">
            Concept
            <textarea
              value={draft.concept}
              onChange={(event) => setDraft({ ...draft, concept: event.target.value })}
            />
          </label>

          <label className="full-span">
            Target audience
            <textarea
              value={draft.target_audience}
              onChange={(event) => setDraft({ ...draft, target_audience: event.target.value })}
            />
          </label>

          <label className="full-span">
            Voice
            <textarea
              value={draft.voice}
              onChange={(event) => setDraft({ ...draft, voice: event.target.value })}
            />
          </label>

          <label className="full-span">
            Current goal
            <textarea
              value={draft.current_goal}
              onChange={(event) => setDraft({ ...draft, current_goal: event.target.value })}
            />
          </label>
        </div>

        <div className="channel-editor">
          {draft.channels.map((channel, index) => (
            <div className="channel-row" key={`${channel.channel}-${index}`}>
              <input
                value={channel.channel}
                onChange={(event) => updateChannel(index, "channel", event.target.value)}
              />
              <input
                value={channel.handle}
                onChange={(event) => updateChannel(index, "handle", event.target.value)}
              />
              <input
                value={channel.focus}
                onChange={(event) => updateChannel(index, "focus", event.target.value)}
              />
            </div>
          ))}
        </div>

        <button className="primary-button" type="submit" disabled={loading}>
          {loading ? "Saving..." : "Save profile"}
        </button>
      </form>
    </section>
  );
}
