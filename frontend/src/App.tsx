import { useCallback, useEffect, useMemo, useState, type FormEvent, type ReactNode } from "react";
import {
  Activity, ArrowDownRight, ArrowUpRight, Bell, BrainCircuit,
  Check, ChevronDown, CircleHelp, Command, FlaskConical, Gauge, Lightbulb,
  MessageSquareText, Plus, RefreshCw, Search, Send, Settings2, Sparkles,
  Target, X,
} from "lucide-react";
import { api } from "./api";
import type { Dashboard, Experiment, Feedback, Opportunity } from "./types";

type Page = "Overview" | "Feedback" | "Opportunities" | "Experiments";
const navigation: { label: Page; icon: typeof Gauge; hint: string }[] = [
  { label: "Overview", icon: Gauge, hint: "Workspace pulse" },
  { label: "Feedback", icon: MessageSquareText, hint: "Voice of customer" },
  { label: "Opportunities", icon: Lightbulb, hint: "Prioritisation" },
  { label: "Experiments", icon: FlaskConical, hint: "Learn & iterate" },
];

function initials(value: string) {
  return value.split(" ").map((part) => part[0]).slice(0, 2).join("").toUpperCase();
}
function sentimentClass(value: string) {
  return value === "positive" ? "positive" : value === "negative" ? "negative" : "neutral";
}
function shortDate(value: string) {
  return new Date(value).toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export default function App() {
  const [page, setPage] = useState<Page>("Overview");
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [feedback, setFeedback] = useState<Feedback[]>([]);
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [query, setQuery] = useState("");
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [showOpportunityForm, setShowOpportunityForm] = useState(false);
  const [showExperimentForm, setShowExperimentForm] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [d, f, o, e] = await Promise.all([
        api.dashboard(), api.feedback(), api.opportunities(), api.experiments(),
      ]);
      setDashboard(d); setFeedback(f); setOpportunities(o); setExperiments(e);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not connect to the API.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void load(); }, [load]);
  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(""), 2800);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const filteredFeedback = useMemo(() => {
    const term = query.toLowerCase();
    return feedback.filter((item) =>
      [item.text, item.theme, item.source, item.segment].some((v) => v.toLowerCase().includes(term)),
    );
  }, [feedback, query]);

  async function handleFeedbackSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    try {
      await api.addFeedback({
        text: String(form.get("text") || ""),
        source: String(form.get("source") || "In-app"),
        segment: String(form.get("segment") || "Unknown"),
      });
      formElement.reset(); setShowFeedbackForm(false); setToast("Feedback added and analysed.");
      await load();
    } catch (err) { setToast(err instanceof Error ? err.message : "Could not save feedback."); }
  }

  async function handleOpportunitySubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    try {
      await api.addOpportunity({
        title: String(form.get("title")), problem_statement: String(form.get("problem_statement")),
        theme: String(form.get("theme")), reach: Number(form.get("reach")),
        impact: Number(form.get("impact")), confidence: Number(form.get("confidence")),
        effort: Number(form.get("effort")), status: "Candidate",
      });
      formElement.reset(); setShowOpportunityForm(false); setToast("Opportunity added to the backlog.");
      await load();
    } catch (err) { setToast(err instanceof Error ? err.message : "Could not save opportunity."); }
  }

  async function handleExperimentSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    try {
      await api.addExperiment({
        title: String(form.get("title")), hypothesis: String(form.get("hypothesis")),
        success_metric: String(form.get("success_metric")), owner: String(form.get("owner")),
        baseline_value: form.get("baseline_value") ? Number(form.get("baseline_value")) : null,
        target_value: form.get("target_value") ? Number(form.get("target_value")) : null,
        status: "Planned",
      });
      formElement.reset(); setShowExperimentForm(false); setToast("Experiment added.");
      await load();
    } catch (err) { setToast(err instanceof Error ? err.message : "Could not save experiment."); }
  }

  async function updateOpportunity(id: number, status: string) {
    try { await api.updateOpportunity(id, status); await load(); setToast("Opportunity status updated."); }
    catch (err) { setToast(err instanceof Error ? err.message : "Update failed."); }
  }
  async function updateExperiment(id: number, status: string) {
    try { await api.updateExperiment(id, status); await load(); setToast("Experiment status updated."); }
    catch (err) { setToast(err instanceof Error ? err.message : "Update failed."); }
  }
  async function resetDemo() {
    if (!window.confirm("Restore the sample workspace? This removes feedback, opportunities and experiments you added.")) return;
    try { await api.reseed(); await load(); setToast("Sample workspace restored."); }
    catch (err) { setToast(err instanceof Error ? err.message : "Could not restore demo."); }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><BrainCircuit size={21} strokeWidth={2.2} /></div>
          <div><strong>stratify<span>ai</span></strong><small>PRODUCT INTELLIGENCE</small></div>
        </div>
        <div className="workspace-switch">
          <div className="workspace-avatar">V</div>
          <div className="workspace-copy"><b>Vaeshaa workspace</b><small>Product team · Free plan</small></div>
          <ChevronDown size={15} />
        </div>
        <div className="side-label">WORKSPACE</div>
        <nav className="nav-list">
          {navigation.map(({ label, icon: Icon, hint }) => (
            <button className={page === label ? "nav-item active" : "nav-item"} key={label} onClick={() => setPage(label)}>
              <Icon size={18} /><span>{label}</span>{label === "Feedback" && <em>{feedback.length}</em>}
              <small>{hint}</small>
            </button>
          ))}
        </nav>
        <div className="side-label tools-label">TOOLS</div>
        <button className="nav-item quiet" onClick={() => setToast("Settings are part of the product roadmap.")}><Settings2 size={18}/><span>Settings</span></button>
        <button className="nav-item quiet" onClick={() => setToast("Help centre coming soon.")}><CircleHelp size={18}/><span>Help centre</span></button>
        <div className="sidebar-bottom">
          <div className="insight-mini">
            <div className="mini-icon"><Sparkles size={16}/></div>
            <b>Turn signals into strategy</b>
            <p>Make every product decision traceable to customer evidence.</p>
            <button onClick={() => setPage("Opportunities")}>Explore opportunities <ArrowUpRight size={13}/></button>
          </div>
          <div className="profile-row">
            <div className="profile-avatar">VP</div><div><b>Product workspace</b><small>Vaeshaa · Admin</small></div><ChevronDown size={14}/>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs"><span>Vaeshaa</span><span className="crumb-slash">/</span><b>{page}</b></div>
          <div className="top-actions">
            <div className="demo-badge"><span/> DEMO WORKSPACE</div>
            <button className="icon-button" aria-label="Search" onClick={() => setPage("Feedback")}><Search size={18}/></button>
            <button className="icon-button notification" aria-label="Notifications" onClick={() => setToast("You're all caught up.")}><Bell size={18}/><i/></button>
            <div className="top-avatar">VP</div>
          </div>
        </header>

        <div className="page-content">
          {error && <div className="connection-banner"><span><strong>API connection unavailable.</strong> Start the FastAPI backend to load live workspace data. {error}</span><button onClick={() => void load()}><RefreshCw size={14}/> Retry</button></div>}
          {loading && !dashboard ? <div className="loading-state"><div className="loader"/><p>Connecting to your product workspace…</p></div> : (
            <>
              {page === "Overview" && dashboard && <Overview dashboard={dashboard} onNavigate={setPage} onAddFeedback={() => setShowFeedbackForm(true)} onReset={resetDemo}/>}
              {page === "Feedback" && <FeedbackPage items={filteredFeedback} query={query} setQuery={setQuery} onAdd={() => setShowFeedbackForm(true)}/>}
              {page === "Opportunities" && <OpportunitiesPage items={opportunities} onAdd={() => setShowOpportunityForm(true)} onStatus={updateOpportunity}/>}
              {page === "Experiments" && <ExperimentsPage items={experiments} onAdd={() => setShowExperimentForm(true)} onStatus={updateExperiment}/>}
            </>
          )}
        </div>
        <footer className="footer"><span>STRATIFYAI <i>•</i> PRODUCT DECISION INTELLIGENCE</span><span>Built for evidence-led product teams <span className="footer-dot">✳</span></span></footer>
      </main>

      {showFeedbackForm && <Modal title="Capture customer feedback" subtitle="Add a voice-of-customer signal to the workspace." onClose={() => setShowFeedbackForm(false)}>
        <form className="form-stack" onSubmit={handleFeedbackSubmit}>
          <label>Feedback <textarea name="text" minLength={8} maxLength={4000} required placeholder="What did the customer say? Include the context…" /></label>
          <div className="form-grid">
            <label>Source<select name="source"><option>In-app</option><option>Support</option><option>Review</option><option>Survey</option><option>Interview</option></select></label>
            <label>Customer segment<select name="segment"><option>SMB</option><option>Mid-market</option><option>Enterprise</option><option>Unknown</option></select></label>
          </div>
          <div className="modal-actions"><button type="button" className="btn-secondary" onClick={() => setShowFeedbackForm(false)}>Cancel</button><button className="btn-primary"><Send size={15}/> Analyse feedback</button></div>
        </form>
      </Modal>}
      {showOpportunityForm && <Modal title="Create opportunity" subtitle="Frame a customer problem before proposing a solution." onClose={() => setShowOpportunityForm(false)}>
        <form className="form-stack" onSubmit={handleOpportunitySubmit}>
          <label>Opportunity title<input name="title" required minLength={4} placeholder="e.g. Reduce setup friction" /></label>
          <label>Customer problem<textarea name="problem_statement" required minLength={8} placeholder="Who experiences this problem, and what is the impact?" /></label>
          <label>Theme<select name="theme"><option>Onboarding</option><option>Reliability</option><option>Workflow</option><option>Reporting</option><option>Pricing</option><option>Other</option></select></label>
          <div className="form-grid four">
            <label>Reach<input name="reach" type="number" min="1" max="100" defaultValue="40" required/><small>Users / period</small></label>
            <label>Impact<input name="impact" type="number" min="0.25" max="3" step="0.25" defaultValue="2" required/><small>0.25–3</small></label>
            <label>Confidence<input name="confidence" type="number" min="0.1" max="1" step="0.05" defaultValue="0.7" required/><small>0.1–1.0</small></label>
            <label>Effort<input name="effort" type="number" min="0.5" max="100" step="0.5" defaultValue="3" required/><small>Person-weeks</small></label>
          </div>
          <div className="modal-actions"><button type="button" className="btn-secondary" onClick={() => setShowOpportunityForm(false)}>Cancel</button><button className="btn-primary"><Plus size={15}/> Add to backlog</button></div>
        </form>
      </Modal>}
      {showExperimentForm && <Modal title="Design an experiment" subtitle="State the hypothesis and the outcome that would change your decision." onClose={() => setShowExperimentForm(false)}>
        <form className="form-stack" onSubmit={handleExperimentSubmit}>
          <label>Experiment name<input name="title" required minLength={4} placeholder="e.g. Guided setup checklist" /></label>
          <label>Hypothesis<textarea name="hypothesis" required minLength={8} placeholder="If we…, then…, because…" /></label>
          <label>Success metric<input name="success_metric" required placeholder="e.g. First-week activation rate" /></label>
          <div className="form-grid">
            <label>Baseline<input name="baseline_value" type="number" step="0.01" placeholder="Optional" /></label>
            <label>Target<input name="target_value" type="number" step="0.01" placeholder="Optional" /></label>
          </div>
          <label>Owner<input name="owner" defaultValue="Product" /></label>
          <div className="modal-actions"><button type="button" className="btn-secondary" onClick={() => setShowExperimentForm(false)}>Cancel</button><button className="btn-primary"><FlaskConical size={15}/> Create experiment</button></div>
        </form>
      </Modal>}
      {toast && <div className="toast"><Check size={16}/>{toast}</div>}
    </div>
  );
}

function Overview({ dashboard, onNavigate, onAddFeedback, onReset }: {
  dashboard: Dashboard; onNavigate: (page: Page) => void; onAddFeedback: () => void; onReset: () => void;
}) {
  const sentimentTotal = Object.values(dashboard.sentiment).reduce((a, b) => a + b, 0) || 1;
  const negativeShare = Math.round(((dashboard.sentiment.negative || 0) / sentimentTotal) * 100);
  const maxTheme = Math.max(1, ...dashboard.themes.map((item) => item.count));
  return <div className="view">
    <div className="page-heading">
      <div><div className="eyebrow"><span className="eyebrow-line"/> PRODUCT SIGNALS <span className="eyebrow-date">/ THIS WORKSPACE</span></div>
        <h1>Good morning, team <span className="wave">✳</span></h1>
        <p>Here's what customers are telling you — and where to focus next.</p></div>
      <div className="heading-actions"><button className="btn-secondary" onClick={onReset}><RefreshCw size={15}/> Reset demo</button><button className="btn-primary" onClick={onAddFeedback}><Plus size={16}/> Add feedback</button></div>
    </div>
    <div className="demo-note"><Sparkles size={15}/><span><b>Illustrative workspace</b> — sample data is synthetic, designed to demonstrate the workflow. Connect real sources to validate these signals.</span></div>

    <section className="metric-grid">
      <MetricCard label="Feedback captured" value={dashboard.feedback_count.toLocaleString()} sub="Across all sample sources" icon={MessageSquareText} color="violet" trend="VOC" />
      <MetricCard label="Negative signals" value={String(dashboard.negative_feedback)} sub={`${negativeShare}% of analysed feedback`} icon={Activity} color="rose" trend={negativeShare >= 50 ? "Review" : "Monitor"} />
      <MetricCard label="Opportunities" value={String(dashboard.opportunity_count)} sub="Prioritised problem statements" icon={Lightbulb} color="amber" trend="Backlog" />
      <MetricCard label="Running experiments" value={String(dashboard.active_experiments)} sub="Learning loops in motion" icon={FlaskConical} color="green" trend="Learn" />
    </section>

    <section className="overview-grid">
      <div className="panel theme-panel">
        <div className="panel-heading"><div><span className="section-kicker">VOICE OF CUSTOMER</span><h2>What customers talk about</h2><p>Feedback themes by volume</p></div><button className="text-link" onClick={() => onNavigate("Feedback")}>View feedback <ArrowUpRight size={14}/></button></div>
        <div className="theme-chart">
          {dashboard.themes.map((item, index) => <div className="theme-row" key={item.theme}>
            <div className="theme-label"><span className={`theme-dot dot-${index % 5}`}/><b>{item.theme}</b><small>{item.count} signals</small></div>
            <div className="theme-track"><div className={`theme-fill fill-${index % 5}`} style={{ width: `${(item.count / maxTheme) * 100}%` }}/></div>
            <div className="theme-value">{Math.round((item.count / Math.max(1, dashboard.feedback_count)) * 100)}%</div>
          </div>)}
          {dashboard.themes.length === 0 && <EmptyState text="Add feedback to reveal customer themes."/>}
        </div>
        <div className="chart-legend"><span><i className="legend-violet"/> Theme volume</span><span><i className="legend-muted"/> Share of feedback</span></div>
      </div>
      <div className="panel sentiment-panel">
        <div className="panel-heading"><div><span className="section-kicker">SENTIMENT PULSE</span><h2>Customer tone</h2><p>Directional baseline classification</p></div><div className="pulse-icon"><Activity size={17}/></div></div>
        <div className="sentiment-content">
          <div className="donut" style={{ background: `conic-gradient(#e66c83 0 ${(dashboard.sentiment.negative || 0) / sentimentTotal * 100}%, #eab96a ${(dashboard.sentiment.negative || 0) / sentimentTotal * 100}% ${((dashboard.sentiment.negative || 0) + (dashboard.sentiment.neutral || 0)) / sentimentTotal * 100}%, #58b99a ${((dashboard.sentiment.negative || 0) + (dashboard.sentiment.neutral || 0)) / sentimentTotal * 100}% 100%)` }}>
            <div><strong>{negativeShare}%</strong><small>negative</small></div>
          </div>
          <div className="sentiment-legend">
            {(["negative", "neutral", "positive"] as const).map((name) => <div key={name}><span className={`sentiment-indicator ${name}`}/><span>{name}</span><b>{dashboard.sentiment[name] || 0}</b></div>)}
          </div>
        </div>
        <div className="insight-callout"><Lightbulb size={15}/><span><b>Read the signal, not just the score.</b> Theme and sentiment labels are heuristic suggestions. Review source feedback before making roadmap decisions.</span></div>
      </div>
    </section>

    <section className="bottom-grid">
      <div className="panel opportunity-panel">
        <div className="panel-heading"><div><span className="section-kicker">DECISION QUEUE</span><h2>Top opportunities</h2><p>Ranked using the RICE framework</p></div><button className="text-link" onClick={() => onNavigate("Opportunities")}>Open backlog <ArrowUpRight size={14}/></button></div>
        <div className="opportunity-list">
          {dashboard.top_opportunities.map((item, index) => <div className="opportunity-row" key={item.id}>
            <div className="rank">0{index + 1}</div><div className="opp-copy"><b>{item.title}</b><small>{item.theme} <span>·</span> {item.status}</small></div><div className="rice-mini"><strong>{item.rice_score}</strong><small>RICE</small></div>
          </div>)}
          {dashboard.top_opportunities.length === 0 && <EmptyState text="Create an opportunity to start prioritising."/>}
        </div>
      </div>
      <div className="panel recent-panel">
        <div className="panel-heading"><div><span className="section-kicker">LATEST SIGNALS</span><h2>Recent feedback</h2><p>Newest customer voices</p></div><button className="text-link" onClick={() => onNavigate("Feedback")}>See all <ArrowUpRight size={14}/></button></div>
        <div className="recent-list">
          {dashboard.recent_feedback.slice(0, 4).map((item) => <div className="recent-item" key={item.id}>
            <div className={`sentiment-icon ${sentimentClass(item.sentiment)}`}>{item.sentiment === "positive" ? <ArrowUpRight size={14}/> : item.sentiment === "negative" ? <ArrowDownRight size={14}/> : <MessageSquareText size={13}/>}</div>
            <div className="recent-copy"><p>{item.text}</p><small>{item.theme} <span>·</span> {item.source}</small></div>
            <time>{shortDate(item.created_at)}</time>
          </div>)}
        </div>
      </div>
    </section>
    <div className="footnote"><span><i/> {dashboard.data_note}</span><button onClick={() => onNavigate("Experiments")}>Go to experiments <ArrowUpRight size={13}/></button></div>
  </div>;
}

function MetricCard({ label, value, sub, icon: Icon, color, trend }: {
  label: string; value: string; sub: string; icon: typeof Gauge; color: string; trend: string;
}) {
  return <div className="metric-card">
    <div className="metric-top"><span>{label}</span><div className={`metric-icon ${color}`}><Icon size={17}/></div></div>
    <div className="metric-value">{value}</div><div className="metric-sub">{sub}</div>
    <div className="metric-bottom"><span className={`tiny-pill ${color}`}>{trend}</span><span className="metric-period">Workspace total</span></div>
  </div>;
}

function FeedbackPage({ items, query, setQuery, onAdd }: {
  items: Feedback[]; query: string; setQuery: (value: string) => void; onAdd: () => void;
}) {
  return <div className="view">
    <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line"/> CUSTOMER DISCOVERY</div><h1>Feedback inbox</h1><p>Capture, categorise and inspect the voice of the customer.</p></div><button className="btn-primary" onClick={onAdd}><Plus size={16}/> Add feedback</button></div>
    <div className="filter-bar"><div className="search-field"><Search size={16}/><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search feedback, themes or segments…" /></div><span className="result-count">{items.length} signals</span></div>
    <div className="panel table-panel"><div className="table-scroll"><table><thead><tr><th>CUSTOMER VOICE</th><th>THEME</th><th>SENTIMENT</th><th>SOURCE</th><th>SEGMENT</th><th>ADDED</th></tr></thead><tbody>
      {items.map((item) => <tr key={item.id}><td className="feedback-cell"><p>{item.text}</p><small>Feedback #{String(item.id).padStart(3, "0")}</small></td><td><span className="theme-chip">{item.theme}</span></td><td><span className={`sentiment-pill ${sentimentClass(item.sentiment)}`}><i/>{item.sentiment}</span></td><td>{item.source}</td><td>{item.segment}</td><td className="muted-cell">{shortDate(item.created_at)}</td></tr>)}
    </tbody></table>{items.length === 0 && <EmptyState text="No matching feedback. Try another search or add a new signal."/>}</div></div>
    <div className="method-note"><BrainCircuit size={16}/><div><b>How classification works</b><p>This MVP uses an explainable keyword baseline to suggest a theme and sentiment. It is intentionally transparent and should be reviewed by a human before prioritisation. It is not a trained production model.</p></div></div>
  </div>;
}

function OpportunitiesPage({ items, onAdd, onStatus }: {
  items: Opportunity[]; onAdd: () => void; onStatus: (id: number, status: string) => void;
}) {
  return <div className="view">
    <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line"/> PRODUCT STRATEGY</div><h1>Opportunity backlog</h1><p>Prioritise customer problems with an explicit, inspectable scoring model.</p></div><button className="btn-primary" onClick={onAdd}><Plus size={16}/> New opportunity</button></div>
    <div className="method-banner"><Target size={18}/><div><b>RICE prioritisation</b><span>Reach × Impact × Confidence ÷ Effort. Scores support comparison; they do not replace product judgment or customer evidence.</span></div><div className="formula">R × I × C / E</div></div>
    <div className="panel table-panel"><div className="table-scroll"><table><thead><tr><th>OPPORTUNITY</th><th>THEME</th><th>REACH</th><th>IMPACT</th><th>CONF.</th><th>EFFORT</th><th>RICE SCORE</th><th>STATUS</th></tr></thead><tbody>
      {items.map((item, index) => <tr key={item.id}><td className="opp-table-cell"><span className="table-rank">{String(index + 1).padStart(2, "0")}</span><div><b>{item.title}</b><small>{item.problem_statement}</small></div></td><td><span className="theme-chip">{item.theme}</span></td><td>{item.reach}</td><td>{item.impact.toFixed(2)}</td><td>{Math.round(item.confidence * 100)}%</td><td>{item.effort}</td><td><strong className="score-value">{item.rice_score.toFixed(1)}</strong></td><td><select className="status-select" value={item.status} onChange={(e) => onStatus(item.id, e.target.value)}><option>Candidate</option><option>Planned</option><option>In progress</option><option>Shipped</option><option>Dropped</option></select></td></tr>)}
    </tbody></table>{items.length === 0 && <EmptyState text="No opportunities yet. Add a customer problem to prioritise it."/>}</div></div>
    <div className="method-note"><Lightbulb size={16}/><div><b>Product judgement matters</b><p>RICE values in this demo are illustrative estimates. In a real product process, agree on scoring definitions, document evidence behind reach and confidence, and revisit scores as new data arrives.</p></div></div>
  </div>;
}

function ExperimentsPage({ items, onAdd, onStatus }: {
  items: Experiment[]; onAdd: () => void; onStatus: (id: number, status: string) => void;
}) {
  return <div className="view">
    <div className="page-heading"><div><div className="eyebrow"><span className="eyebrow-line"/> CONTINUOUS DISCOVERY</div><h1>Experiment tracker</h1><p>Turn product assumptions into testable hypotheses and measurable learning.</p></div><button className="btn-primary" onClick={onAdd}><Plus size={16}/> New experiment</button></div>
    <div className="experiment-summary"><div><span className="summary-icon running"><Activity size={17}/></span><div><b>{items.filter((item) => item.status === "Running").length}</b><small>Running</small></div></div><div><span className="summary-icon planned"><Target size={17}/></span><div><b>{items.filter((item) => item.status === "Planned").length}</b><small>Planned</small></div></div><div><span className="summary-icon completed"><Check size={17}/></span><div><b>{items.filter((item) => item.status === "Completed").length}</b><small>Completed</small></div></div></div>
    <div className="experiment-grid">
      {items.map((item) => {
        const progress = item.baseline_value !== null && item.target_value !== null && item.target_value !== item.baseline_value
          ? Math.min(100, Math.max(0, Math.round((item.baseline_value / item.target_value) * 100))) : 0;
        return <div className="panel experiment-card" key={item.id}>
          <div className="experiment-card-top"><span className={`status-tag ${item.status.toLowerCase().replace(" ", "-")}`}>{item.status}</span><span className="experiment-id">EXP-{String(item.id).padStart(3, "0")}</span></div>
          <h3>{item.title}</h3><div className="hypothesis-label">HYPOTHESIS</div><p className="hypothesis-text">{item.hypothesis}</p>
          <div className="experiment-metric"><div><small>SUCCESS METRIC</small><b>{item.success_metric}</b></div><div className="owner-avatar">{initials(item.owner || "PM")}</div></div>
          {item.baseline_value !== null && item.target_value !== null && <div className="experiment-progress"><div className="progress-label"><span>Baseline <b>{item.baseline_value}</b></span><span>Target <b>{item.target_value}</b></span></div><div className="progress-track"><div style={{ width: `${progress}%` }}/></div></div>}
          <div className="experiment-card-footer"><span>Owner · {item.owner}</span><select className="status-select" value={item.status} onChange={(e) => onStatus(item.id, e.target.value)}><option>Planned</option><option>Running</option><option>Completed</option><option>Paused</option></select></div>
        </div>;
      })}
    </div>
    {items.length === 0 && <div className="panel"><EmptyState text="No experiments yet. Add a hypothesis and success metric to start learning."/></div>}
    <div className="method-note"><FlaskConical size={16}/><div><b>Experiment discipline</b><p>Before running a test, define eligibility, sample size, guardrail metrics, decision threshold and duration. This tracker records plans and status; it does not claim statistical significance or calculate causal lift.</p></div></div>
  </div>;
}

function Modal({ title, subtitle, onClose, children }: {
  title: string; subtitle: string; onClose: () => void; children: ReactNode;
}) {
  return <div className="modal-backdrop" onMouseDown={(e) => { if (e.target === e.currentTarget) onClose(); }}>
    <div className="modal"><div className="modal-heading"><div><h2>{title}</h2><p>{subtitle}</p></div><button className="icon-button" onClick={onClose} aria-label="Close"><X size={18}/></button></div>{children}</div>
  </div>;
}
function EmptyState({ text }: { text: string }) {
  return <div className="empty-state"><div><Command size={19}/></div><p>{text}</p></div>;
}
