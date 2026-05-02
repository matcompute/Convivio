import { useState } from "react";

export function ReviewDesk({ reviews, onRespond, loading }) {
  const [tones, setTones] = useState(() =>
    Object.fromEntries(reviews.map((item) => [item.id, "warm"])),
  );
  const [offers, setOffers] = useState(() =>
    Object.fromEntries(reviews.map((item) => [item.id, "A return visit with a welcome amuse-bouche"])),
  );

  return (
    <section className="view-stack">
      <section className="surface">
        <div className="surface-header">
          <h3>Review desk</h3>
          <span>{reviews.length} guest signals</span>
        </div>

        <div className="review-grid">
          {reviews.map((review) => (
            <article className="review-card" key={review.id}>
              <div className="review-head">
                <div>
                  <strong>{review.guest_name}</strong>
                  <small>
                    {review.source} • {review.rating}/5 • {review.sentiment}
                  </small>
                </div>
                <span>{review.status}</span>
              </div>

              <p>{review.review_text}</p>
              <label>
                Tone
                <select
                  value={tones[review.id] ?? "warm"}
                  onChange={(event) =>
                    setTones((current) => ({ ...current, [review.id]: event.target.value }))
                  }
                >
                  <option value="warm">Warm</option>
                  <option value="apologetic">Apologetic</option>
                  <option value="confident">Confident</option>
                  <option value="celebratory">Celebratory</option>
                </select>
              </label>

              <label>
                Recovery offer
                <input
                  value={offers[review.id] ?? ""}
                  onChange={(event) =>
                    setOffers((current) => ({ ...current, [review.id]: event.target.value }))
                  }
                />
              </label>

              <button
                type="button"
                className="secondary-button"
                disabled={loading}
                onClick={() =>
                  onRespond({
                    review_id: review.id,
                    tone: tones[review.id] ?? "warm",
                    recovery_offer: offers[review.id] ?? "",
                  })
                }
              >
                Draft response
              </button>

              {review.drafted_response ? (
                <div className="response-preview">
                  <span>Drafted response</span>
                  <p>{review.drafted_response}</p>
                </div>
              ) : null}
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
