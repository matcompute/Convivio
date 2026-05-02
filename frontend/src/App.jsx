import { useEffect, useMemo, useState } from "react";
import { CampaignStudio } from "./components/CampaignStudio";
import { LoginView } from "./components/LoginView";
import { OverviewPanel } from "./components/OverviewPanel";
import { ProfilePanel } from "./components/ProfilePanel";
import { RetentionLab } from "./components/RetentionLab";
import { ReviewDesk } from "./components/ReviewDesk";

const tokenKey = "convivio_token";
const defaultLogin = { email: "owner@convivio.io", password: "Convivio123!" };
const navigation = [
  { id: "overview", label: "Overview" },
  { id: "campaigns", label: "Campaign Studio" },
  { id: "reviews", label: "Review Desk" },
  { id: "retention", label: "Retention Lab" },
  { id: "profile", label: "Brand Profile" },
];

async function apiRequest(path, options = {}, token) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed." }));
    throw new Error(error.detail || "Request failed.");
  }

  return response.json();
}

export default function App() {
  const [token, setToken] = useState(() => window.localStorage.getItem(tokenKey) || "");
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [dashboard, setDashboard] = useState({ metrics: [], active_objectives: [], highlights: [] });
  const [campaigns, setCampaigns] = useState([]);
  const [reviews, setReviews] = useState([]);
  const [plans, setPlans] = useState([]);
  const [loginForm, setLoginForm] = useState(defaultLogin);
  const [activeView, setActiveView] = useState("overview");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const workspaceTitle = useMemo(() => profile?.name || "Convivio", [profile]);

  async function loadWorkspace(currentToken) {
    const [me, loadedProfile, loadedDashboard, loadedCampaigns, loadedReviews, loadedPlans] =
      await Promise.all([
        apiRequest("/api/auth/me", {}, currentToken),
        apiRequest("/api/business/profile", {}, currentToken),
        apiRequest("/api/dashboard", {}, currentToken),
        apiRequest("/api/campaigns", {}, currentToken),
        apiRequest("/api/reviews", {}, currentToken),
        apiRequest("/api/retention/plans", {}, currentToken),
      ]);

    setUser(me);
    setProfile(loadedProfile);
    setDashboard(loadedDashboard);
    setCampaigns(loadedCampaigns);
    setReviews(loadedReviews);
    setPlans(loadedPlans);
  }

  useEffect(() => {
    if (!token) {
      return;
    }

    let cancelled = false;
    setBusy(true);
    setError("");

    loadWorkspace(token)
      .catch((loadError) => {
        if (!cancelled) {
          setToken("");
          window.localStorage.removeItem(tokenKey);
          setError(loadError.message);
        }
      })
      .finally(() => {
        if (!cancelled) {
          setBusy(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  const handleLogin = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError("");

    try {
      const result = await apiRequest("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(loginForm),
      });
      setToken(result.access_token);
      window.localStorage.setItem(tokenKey, result.access_token);
    } catch (loginError) {
      setError(loginError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleLogout = () => {
    setToken("");
    setUser(null);
    setProfile(null);
    setCampaigns([]);
    setReviews([]);
    setPlans([]);
    window.localStorage.removeItem(tokenKey);
  };

  const handleCampaignGenerate = async (payload) => {
    setBusy(true);
    setError("");

    try {
      const campaign = await apiRequest(
        "/api/campaigns/generate",
        { method: "POST", body: JSON.stringify(payload) },
        token,
      );
      setCampaigns((current) => [campaign, ...current]);
      setDashboard(await apiRequest("/api/dashboard", {}, token));
      setActiveView("campaigns");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleCampaignApprove = async (campaignId) => {
    setBusy(true);
    setError("");

    try {
      const result = await apiRequest(`/api/campaigns/${campaignId}/approve`, { method: "POST" }, token);
      setCampaigns((current) => current.map((item) => (item.id === campaignId ? result.campaign : item)));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleReviewResponse = async (payload) => {
    setBusy(true);
    setError("");

    try {
      const result = await apiRequest("/api/reviews/respond", { method: "POST", body: JSON.stringify(payload) }, token);
      setReviews((current) => current.map((item) => (item.id === result.review.id ? result.review : item)));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleRetentionGenerate = async (payload) => {
    setBusy(true);
    setError("");

    try {
      const plan = await apiRequest("/api/retention/generate", { method: "POST", body: JSON.stringify(payload) }, token);
      setPlans((current) => [plan, ...current]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  const handleProfileSave = async (payload) => {
    setBusy(true);
    setError("");

    try {
      const updatedProfile = await apiRequest("/api/business/profile", { method: "PUT", body: JSON.stringify(payload) }, token);
      setProfile(updatedProfile);
      setDashboard(await apiRequest("/api/dashboard", {}, token));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setBusy(false);
    }
  };

  if (!token) {
    return <LoginView form={loginForm} setForm={setLoginForm} onSubmit={handleLogin} error={error} loading={busy} />;
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <span className="eyebrow">Hospitality AI</span>
          <h1>Convivio</h1>
          <p>{workspaceTitle}</p>
        </div>

        <nav className="nav-list">
          {navigation.map((item) => (
            <button
              key={item.id}
              type="button"
              className={activeView === item.id ? "nav-item active" : "nav-item"}
              onClick={() => setActiveView(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <strong>{user?.full_name}</strong>
          <span>{user?.role}</span>
          <button type="button" className="ghost-button" onClick={handleLogout}>
            Sign out
          </button>
        </div>
      </aside>

      <main className="workspace">
        <header className="workspace-header">
          <div>
            <span className="eyebrow">AI workspace</span>
            <h2>{navigation.find((item) => item.id === activeView)?.label}</h2>
          </div>
          <div className="workspace-badges">
            <span>LLM-ready</span>
            <span>Agent-assisted</span>
            <span>Brand-grounded</span>
          </div>
        </header>

        {error ? <p className="error-banner inline">{error}</p> : null}

        {activeView === "overview" ? (
          <OverviewPanel dashboard={dashboard} campaigns={campaigns} reviews={reviews} plans={plans} />
        ) : null}
        {activeView === "campaigns" ? (
          <CampaignStudio campaigns={campaigns} onGenerate={handleCampaignGenerate} onApprove={handleCampaignApprove} loading={busy} />
        ) : null}
        {activeView === "reviews" ? <ReviewDesk reviews={reviews} onRespond={handleReviewResponse} loading={busy} /> : null}
        {activeView === "retention" ? (
          <RetentionLab plans={plans} onGenerate={handleRetentionGenerate} loading={busy} />
        ) : null}
        {activeView === "profile" ? <ProfilePanel profile={profile} onSave={handleProfileSave} loading={busy} /> : null}
      </main>
    </div>
  );
}
