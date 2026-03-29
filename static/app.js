/* ══════════════════════════════════════════════════════════════════════════════
   NEXUS Sales OS — Frontend Application
   SPA with hash routing, API client, page renderers, charts, typing effects
   ══════════════════════════════════════════════════════════════════════════════ */

const API = {
    base: '/api',

    async get(path) {
        const res = await fetch(this.base + path);
        if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
        return res.json();
    },

    async post(path, body = {}) {
        const res = await fetch(this.base + path, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`);
        return res.json();
    }
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function formatCurrency(val) {
    if (val >= 10000000) return '₹' + (val / 10000000).toFixed(2) + ' Cr';
    if (val >= 100000) return '₹' + (val / 100000).toFixed(2) + ' L';
    return '₹' + val.toLocaleString('en-IN');
}

function getRiskClass(score) {
    if (score >= 70) return 'high';
    if (score >= 40) return 'medium';
    return 'low';
}

function getRiskLabel(score) {
    if (score >= 70) return 'High Risk';
    if (score >= 40) return 'Medium Risk';
    return 'Low Risk';
}

function getRiskEmoji(score) {
    if (score >= 70) return '🔴';
    if (score >= 40) return '🟡';
    return '🟢';
}

function timeAgo(dateStr) {
    if (!dateStr) return 'N/A';
    const d = new Date(dateStr);
    const now = new Date();
    const days = Math.floor((now - d) / (1000 * 60 * 60 * 24));
    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    return `${days} days ago`;
}

function typeText(element, text, speed = 12) {
    return new Promise(resolve => {
        let i = 0;
        element.innerHTML = '';
        const cursor = document.createElement('span');
        cursor.className = 'typing-cursor';
        element.appendChild(cursor);

        function type() {
            if (i < text.length) {
                const char = text.charAt(i);
                if (char === '\n') {
                    element.insertBefore(document.createElement('br'), cursor);
                } else {
                    element.insertBefore(document.createTextNode(char), cursor);
                }
                i++;
                setTimeout(type, speed);
            } else {
                setTimeout(() => {
                    cursor.remove();
                    resolve();
                }, 500);
            }
        }
        type();
    });
}

function renderHealthGauge(score, size = 120) {
    const radius = 46;
    const circumference = 2 * Math.PI * radius;
    const pct = score / 100;
    const offset = circumference * (1 - pct);

    let color;
    if (score >= 70) color = '#10b981';
    else if (score >= 40) color = '#f59e0b';
    else color = '#ef4444';

    return `
        <div class="health-gauge" style="width:${size}px;height:${size}px">
            <svg viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="${radius}" class="bg-ring"/>
                <circle cx="60" cy="60" r="${radius}" class="score-ring"
                    stroke="${color}"
                    stroke-dasharray="${circumference}"
                    stroke-dashoffset="${offset}"/>
            </svg>
            <div class="score-text">
                <span class="score-number" style="color:${color}">${score}</span>
                <span class="score-label">Health</span>
            </div>
        </div>
    `;
}

function renderStageChart(dist, values) {
    const stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost'];
    const colors = ['#6366f1', '#818cf8', '#a855f7', '#c084fc', '#10b981', '#ef4444'];
    const maxVal = Math.max(...Object.values(values), 1);

    return `
        <div class="stage-chart">
            ${stages.map((stage, i) => {
                const count = dist[stage] || 0;
                const value = values[stage] || 0;
                const pct = (value / maxVal) * 100;
                return `
                    <div class="stage-bar-wrap">
                        <span class="stage-bar-label">${stage}</span>
                        <div class="stage-bar-track">
                            <div class="stage-bar-fill" style="width:${Math.max(pct, count > 0 ? 8 : 0)}%;background:${colors[i]}">${count > 0 ? count : ''}</div>
                        </div>
                        <span class="stage-bar-value">${count > 0 ? formatCurrency(value) : '—'}</span>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

const pages = {
    dashboard: { title: 'Dashboard', desc: 'Pipeline Intelligence Overview', render: renderDashboard },
    deals: { title: 'Deal Intelligence', desc: 'AI-Powered Deal Analysis', render: renderDeals },
    prospects: { title: 'Prospecting', desc: 'ICP Scoring & Outreach Sequences', render: renderProspects },
    retention: { title: 'Revenue Retention', desc: 'Churn Prediction & Intervention', render: renderRetention },
    competitive: { title: 'Competitive Intel', desc: 'Battlecards & Objection Handlers', render: renderCompetitive },
    audit: { title: 'Audit Logs', desc: 'AI Decision Trail', render: renderAudit }
};

function navigate(page) {
    const p = pages[page];
    if (!p) return navigate('dashboard');

    $('#page-title').textContent = p.title;
    $('#page-description').textContent = p.desc;

    $$('.nav-item').forEach(n => n.classList.remove('active'));
    const navEl = $(`#nav-${page}`);
    if (navEl) navEl.classList.add('active');

    $('#content-area').innerHTML = '<div class="spinner"></div>';
    p.render();
}

window.addEventListener('hashchange', () => {
    const page = location.hash.slice(1) || 'dashboard';
    navigate(page);
});

function openModal(title, contentHtml) {
    $('#modal-title').textContent = title;
    $('#modal-body').innerHTML = contentHtml;
    $('#modal-overlay').classList.add('active');
}

function closeModal() {
    $('#modal-overlay').classList.remove('active');
}

$('#modal-close').addEventListener('click', closeModal);
$('#modal-overlay').addEventListener('click', (e) => {
    if (e.target === $('#modal-overlay')) closeModal();
});

async function renderDashboard() {
    try {
        const data = await API.get('/dashboard-summary');

        $('#content-area').innerHTML = `
            <div class="stats-grid">
                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">Total Pipeline</span>
                        <div class="card-icon purple">📊</div>
                    </div>
                    <div class="card-value">${formatCurrency(data.total_pipeline_value)}</div>
                    <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px">${data.active_deals} active deals</p>
                </div>
                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">Weighted Pipeline</span>
                        <div class="card-icon blue">📈</div>
                    </div>
                    <div class="card-value">${formatCurrency(data.weighted_pipeline_value)}</div>
                    <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px">Probability-adjusted value</p>
                </div>
                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">Revenue at Risk</span>
                        <div class="card-icon red">⚠️</div>
                    </div>
                    <div class="card-value danger">${formatCurrency(data.revenue_at_risk)}</div>
                    <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px">${data.at_risk_count} deal(s) at risk</p>
                </div>
                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">Prospects</span>
                        <div class="card-icon cyan">🎯</div>
                    </div>
                    <div class="card-value">${data.prospects_count}</div>
                    <p style="font-size:0.75rem;color:var(--text-muted);margin-top:8px">${data.customers_count} active customer(s)</p>
                </div>
            </div>

            <div class="content-grid">
                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">Stage Distribution</span>
                    </div>
                    ${renderStageChart(data.stage_distribution, data.stage_values)}
                </div>

                <div class="card animate-in">
                    <div class="card-header">
                        <span class="card-title">At-Risk Deals</span>
                        <span class="risk-badge high"><span class="risk-dot high"></span>Needs Attention</span>
                    </div>
                    ${data.at_risk_deals.length > 0 ? `
                        <div style="display:flex;flex-direction:column;gap:12px">
                            ${data.at_risk_deals.map(d => `
                                <div style="display:flex;align-items:center;justify-content:space-between;padding:12px;background:var(--bg-glass);border-radius:var(--radius-sm);cursor:pointer"
                                     onclick="location.hash='deals'">
                                    <div>
                                        <div style="font-weight:600;font-size:0.9rem">${d.company}</div>
                                        <div style="font-size:0.75rem;color:var(--text-muted)">${d.client_name} · ${d.stage}</div>
                                    </div>
                                    <div style="text-align:right">
                                        <div style="font-weight:700;font-size:0.9rem">${formatCurrency(d.deal_value)}</div>
                                        <span class="risk-badge ${getRiskClass(d.risk_score)}">${getRiskEmoji(d.risk_score)} ${d.risk_score}/100</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    ` : '<div class="empty-state"><div class="empty-state-icon">✅</div><p class="empty-state-text">No deals at risk. Pipeline is healthy!</p></div>'}
                </div>
            </div>

            <div class="card animate-in full-width">
                <div class="card-header">
                    <span class="card-title">Quick Actions</span>
                </div>
                <div style="display:flex;gap:12px;flex-wrap:wrap">
                    <button class="btn btn-primary" onclick="runPipelineAnalysis()">🔍 Run Pipeline Analysis</button>
                    <button class="btn btn-secondary" onclick="location.hash='deals'">📋 View All Deals</button>
                    <button class="btn btn-secondary" onclick="location.hash='prospects'">🎯 View Prospects</button>
                    <button class="btn btn-secondary" onclick="location.hash='retention'">💚 Retention Dashboard</button>
                </div>
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error loading dashboard: ${error.message}</p></div>`;
    }
}

async function runPipelineAnalysis() {
    openModal('Pipeline Intelligence Analysis', '<div class="spinner"></div><p style="text-align:center;color:var(--text-muted);margin-top:12px">AI agents analyzing pipeline...</p>');

    try {
        const data = await API.post('/pipeline-analysis');

        let html = `
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px">
                <div style="text-align:center;padding:16px;background:var(--bg-glass);border-radius:var(--radius-sm)">
                    <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Pipeline Health</div>
                    <div style="font-size:1.3rem;font-weight:800;color:${data.pipeline_health === 'Critical' ? 'var(--risk-high)' : data.pipeline_health === 'Fair' ? 'var(--risk-medium)' : 'var(--accent-emerald)'}">${data.pipeline_health}</div>
                </div>
                <div style="text-align:center;padding:16px;background:var(--bg-glass);border-radius:var(--radius-sm)">
                    <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Avg Days in Stage</div>
                    <div style="font-size:1.3rem;font-weight:800;color:var(--text-primary)">${data.avg_days_in_stage}</div>
                </div>
                <div style="text-align:center;padding:16px;background:var(--bg-glass);border-radius:var(--radius-sm)">
                    <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px">Revenue at Risk</div>
                    <div style="font-size:1.3rem;font-weight:800;color:var(--risk-high)">${data.revenue_at_risk_pct}%</div>
                </div>
            </div>
        `;

        if (data.bottlenecks.length > 0) {
            html += `<h3 style="font-size:0.9rem;font-weight:700;margin-bottom:12px;color:var(--risk-medium)">⚠️ Bottlenecks Detected</h3>`;
            data.bottlenecks.forEach(b => {
                html += `
                    <div class="risk-factor-item ${b.severity}" style="margin-bottom:10px">
                        <div style="flex:1">
                            <div class="risk-factor-name">${b.company} — ${b.client}</div>
                            <div class="risk-factor-detail">Stuck in ${b.stage} for ${b.days_in_stage} days (${b.days_overdue} days overdue) · ${formatCurrency(b.deal_value)}</div>
                        </div>
                    </div>
                `;
            });
        }

        if (data.suggested_actions.length > 0) {
            html += `<h3 style="font-size:0.9rem;font-weight:700;margin:20px 0 12px;color:var(--text-primary)">🎯 Suggested Actions</h3>`;
            data.suggested_actions.forEach(a => {
                html += `
                    <div class="strategy-item">
                        <div class="strategy-priority ${a.priority}">${a.priority[0].toUpperCase()}</div>
                        <div>
                            <div class="strategy-action-title">${a.action}</div>
                            <div class="strategy-action-desc">${a.details || ''}</div>
                        </div>
                    </div>
                `;
            });
        }

        // AI Reasoning with typing effect
        html += `
            <div class="ai-typing-container" style="margin-top:20px">
                <div class="ai-typing-header">
                    <div class="ai-typing-dots"><span></span><span></span><span></span></div>
                    Pipeline Intelligence Agent — Analysis
                </div>
                <div class="ai-typing-text" id="pipeline-reasoning"></div>
            </div>
        `;

        $('#modal-body').innerHTML = html;
        const reasoningEl = document.getElementById('pipeline-reasoning');
        if (reasoningEl) typeText(reasoningEl, data.reasoning, 8);

    } catch (error) {
        $('#modal-body').innerHTML = `<p style="color:var(--risk-high)">Error: ${error.message}</p>`;
    }
}

async function renderDeals() {
    try {
        const data = await API.get('/deals');
        const deals = data.deals;

        $('#content-area').innerHTML = `
            <div class="section-header">
                <div>
                    <h2 class="section-title">Deal Intelligence</h2>
                    <p class="section-subtitle">Click any deal to run multi-agent AI analysis</p>
                </div>
            </div>

            <div class="card animate-in">
                <table class="data-table" id="deals-table">
                    <thead>
                        <tr>
                            <th>Deal</th>
                            <th>Value</th>
                            <th>Stage</th>
                            <th>Days</th>
                            <th>Last Contact</th>
                            <th>Risk</th>
                            <th>Health Score</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${deals.map(d => `
                            <tr>
                                <td>
                                    <div class="company-cell">
                                        <span class="company-name">${d.company}</span>
                                        <span class="client-name">${d.client_name}</span>
                                    </div>
                                </td>
                                <td style="font-weight:600">${formatCurrency(d.deal_value)}</td>
                                <td><span class="risk-badge low" style="background:rgba(99,102,241,0.1);color:#a5b4fc">${d.stage}</span></td>
                                <td>${d.days_in_stage}d</td>
                                <td>${timeAgo(d.last_contact_date)}</td>
                                <td><span class="risk-badge ${getRiskClass(d.risk_score)}">${getRiskEmoji(d.risk_score)} ${d.risk_score}</span></td>
                                <td>${renderHealthGauge(100 - d.risk_score, 60)}</td>
                                <td>
                                    <button class="btn btn-primary btn-sm" onclick="analyzeDeal('${d.id}')">🤖 Analyze</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error: ${error.message}</p></div>`;
    }
}

async function analyzeDeal(dealId) {
    openModal('AI Deal Analysis', `
        <div style="text-align:center;padding:40px">
            <div class="spinner"></div>
            <p style="color:var(--text-muted);margin-top:16px">Running multi-agent analysis pipeline...</p>
            <div class="agent-pipeline" id="agent-pipeline" style="margin-top:24px;text-align:left;max-width:400px;margin-left:auto;margin-right:auto"></div>
        </div>
    `);

    // Animate pipeline steps
    const agentNames = ['Signal Agent', 'Deal Intelligence Agent', 'Strategy Agent', 'Outreach Agent', 'Revenue Impact Agent', 'Competitive Intelligence Agent'];
    const pipelineEl = document.getElementById('agent-pipeline');

    for (let i = 0; i < agentNames.length; i++) {
        pipelineEl.innerHTML += `
            <div class="agent-step running" id="agent-step-${i}">
                <div class="agent-step-number">${i + 1}</div>
                <span class="agent-step-name">${agentNames[i]}</span>
                <span class="agent-step-status">running...</span>
            </div>
        `;
        await new Promise(r => setTimeout(r, 300));
    }

    try {
        const data = await API.post('/analyze-deal', { deal_id: dealId });

        // Mark all steps complete
        for (let i = 0; i < agentNames.length; i++) {
            const step = document.getElementById(`agent-step-${i}`);
            if (step) {
                step.classList.remove('running');
                step.classList.add('complete');
                step.querySelector('.agent-step-status').textContent = '✓ complete';
            }
        }

        await new Promise(r => setTimeout(r, 500));

        const di = data.deal_intelligence;
        const strat = data.strategy;
        const rev = data.revenue_impact;
        const out = data.outreach;
        const comp = data.competitive_intelligence;

        let html = `
            <!-- Deal Summary + Health -->
            <div style="display:grid;grid-template-columns:1fr auto;gap:24px;margin-bottom:24px;align-items:center">
                <div>
                    <h3 style="font-size:1.2rem;font-weight:800;margin-bottom:4px">${data.deal_summary.company}</h3>
                    <p style="font-size:0.83rem;color:var(--text-muted)">${data.deal_summary.client} · ${data.deal_summary.stage} · ${formatCurrency(data.deal_summary.deal_value)}</p>
                    <div style="display:flex;gap:12px;margin-top:12px">
                        <span class="risk-badge ${getRiskClass(di.risk_score)}">${getRiskEmoji(di.risk_score)} Risk: ${di.risk_score}/100</span>
                        <span class="risk-badge ${getRiskClass(100 - di.deal_health_score)}" style="background:rgba(16,185,129,0.1);color:var(--accent-emerald)">Health: ${di.deal_health_score}/100</span>
                    </div>
                </div>
                ${renderHealthGauge(di.deal_health_score, 100)}
            </div>

            <!-- Revenue Impact -->
            <div class="revenue-impact" style="margin-bottom:24px">
                <div class="saved-label">💰 Revenue Saved by AI</div>
                <div class="saved-value">${rev.revenue_saved_display}</div>
                <div class="saved-detail">ROI: ${rev.roi_percentage}x return on intervention effort</div>
                <div class="revenue-flow">
                    <div class="flow-item">
                        <div class="flow-label">Before AI</div>
                        <div class="flow-value" style="color:var(--risk-high)">${formatCurrency(rev.expected_revenue_before)}</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-item">
                        <div class="flow-label">After AI</div>
                        <div class="flow-value" style="color:var(--accent-emerald)">${formatCurrency(rev.expected_revenue_after)}</div>
                    </div>
                    <div class="flow-arrow">→</div>
                    <div class="flow-item">
                        <div class="flow-label">Recovered</div>
                        <div class="flow-value" style="color:var(--accent-emerald)">${formatCurrency(rev.revenue_recovered)}</div>
                    </div>
                </div>
                <p style="font-size:0.75rem;color:var(--text-muted);margin-top:12px">${rev.impact_summary.probability_change}</p>
            </div>

            <!-- Risk Factors -->
            ${di.risk_factors.length > 0 ? `
                <h3 style="font-size:0.95rem;font-weight:700;margin-bottom:12px">⚠️ Risk Factors</h3>
                ${di.risk_factors.map(rf => `
                    <div class="risk-factor-item ${rf.severity}">
                        <div style="flex:1">
                            <div class="risk-factor-name">${rf.factor}</div>
                            <div class="risk-factor-detail">${rf.detail}</div>
                        </div>
                        <span class="risk-factor-impact" style="background:${rf.severity === 'critical' ? 'var(--risk-high-bg)' : 'var(--risk-medium-bg)'};color:${rf.severity === 'critical' ? 'var(--risk-high)' : 'var(--risk-medium)'}">+${rf.impact}</span>
                    </div>
                `).join('')}
            ` : ''}

            ${di.positive_factors.length > 0 ? `
                <h3 style="font-size:0.95rem;font-weight:700;margin:20px 0 12px">✅ Positive Signals</h3>
                <ul style="list-style:none;padding:0">
                    ${di.positive_factors.map(pf => `<li style="padding:6px 0;font-size:0.83rem;color:var(--accent-emerald)">✓ ${pf}</li>`).join('')}
                </ul>
            ` : ''}

            <!-- AI Reasoning -->
            <div class="ai-typing-container" style="margin:20px 0">
                <div class="ai-typing-header">
                    <div class="ai-typing-dots"><span></span><span></span><span></span></div>
                    Deal Intelligence Agent — AI Reasoning
                </div>
                <div class="ai-typing-text" id="deal-reasoning"></div>
            </div>

            <!-- Strategy -->
            <h3 style="font-size:0.95rem;font-weight:700;margin:24px 0 12px">🎯 Recovery Strategy: ${strat.primary_strategy}</h3>
            <p style="font-size:0.75rem;color:var(--text-muted);margin-bottom:12px">Urgency: <span style="color:${strat.urgency === 'critical' ? 'var(--risk-high)' : strat.urgency === 'high' ? 'var(--risk-medium)' : 'var(--accent-emerald)'};font-weight:700;text-transform:uppercase">${strat.urgency}</span></p>
            ${strat.strategies.map(s => `
                <div class="strategy-item">
                    <div class="strategy-priority ${s.priority}">${s.priority[0].toUpperCase()}</div>
                    <div>
                        <div class="strategy-action-title">${s.action}</div>
                        <div class="strategy-action-desc">${s.description}</div>
                        <div class="strategy-meta">
                            <span>⏰ ${s.timeline}</span>
                            <span>📈 ${s.expected_impact}</span>
                        </div>
                    </div>
                </div>
            `).join('')}

            <!-- Outreach Messages -->
            <h3 style="font-size:0.95rem;font-weight:700;margin:24px 0 12px">📧 Generated Outreach</h3>

            <div class="outreach-card">
                <div class="outreach-card-header"><span class="outreach-channel email">📧 Email</span></div>
                <div class="outreach-card-body">
                    <div class="outreach-subject">Subject: ${out.messages.email.subject}</div>
                    ${out.messages.email.body}
                </div>
            </div>

            <div class="outreach-card">
                <div class="outreach-card-header"><span class="outreach-channel whatsapp">💬 WhatsApp</span></div>
                <div class="outreach-card-body">${out.messages.whatsapp.message}</div>
            </div>

            <div class="outreach-card">
                <div class="outreach-card-header"><span class="outreach-channel linkedin">🔗 LinkedIn</span></div>
                <div class="outreach-card-body">${out.messages.linkedin.message}</div>
            </div>

            <!-- Agent Pipeline -->
            <h3 style="font-size:0.95rem;font-weight:700;margin:24px 0 12px">🤖 Agent Pipeline (${data.agents_executed} agents executed)</h3>
            <div class="agent-pipeline">
                ${data.pipeline_log.map(step => `
                    <div class="agent-step complete">
                        <div class="agent-step-number">${step.step}</div>
                        <span class="agent-step-name">${step.agent}</span>
                        <span class="agent-step-status">✓ ${step.status}</span>
                    </div>
                `).join('')}
            </div>
        `;

        $('#modal-body').innerHTML = html;

        // Trigger typing effect
        const reasoningEl = document.getElementById('deal-reasoning');
        if (reasoningEl) typeText(reasoningEl, di.reasoning, 8);

    } catch (error) {
        $('#modal-body').innerHTML = `<p style="color:var(--risk-high)">Error: ${error.message}</p>`;
    }
}

async function renderProspects() {
    try {
        const data = await API.get('/prospects');

        $('#content-area').innerHTML = `
            <div class="section-header">
                <div>
                    <h2 class="section-title">Prospecting Intelligence</h2>
                    <p class="section-subtitle">ICP scoring, engagement analysis, and outreach sequences</p>
                </div>
            </div>

            <div class="content-grid">
                ${data.prospects.map(p => `
                    <div class="prospect-card animate-in" id="prospect-${p.id}">
                        <div class="prospect-header">
                            <div>
                                <div class="prospect-company">${p.company}</div>
                                <div class="prospect-contact">${p.contact_name}</div>
                            </div>
                            <div class="card-icon ${p.size === 'Enterprise' ? 'purple' : p.size === 'Mid-Market' ? 'blue' : 'green'}" style="width:36px;height:36px;font-size:0.65rem;font-weight:700">${p.size.slice(0, 3)}</div>
                        </div>
                        <div class="prospect-meta">
                            <div class="prospect-meta-item"><span class="prospect-meta-label">Industry</span>${p.industry}</div>
                            <div class="prospect-meta-item"><span class="prospect-meta-label">Signals</span>${p.engagement_signals.length}</div>
                            <div class="prospect-meta-item"><span class="prospect-meta-label">Site Visits</span>${p.website_visits}</div>
                        </div>
                        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px">
                            ${p.engagement_signals.map(s => `<span style="font-size:0.68rem;padding:3px 8px;background:var(--bg-glass);border-radius:10px;color:var(--text-muted)">${s}</span>`).join('')}
                        </div>
                        <button class="btn btn-primary btn-sm" style="width:100%" onclick="analyzeProspect('${p.id}')">🎯 Analyze & Generate Outreach</button>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error: ${error.message}</p></div>`;
    }
}

async function analyzeProspect(prospectId) {
    openModal('Prospect Analysis', '<div class="spinner"></div><p style="text-align:center;color:var(--text-muted);margin-top:12px">Analyzing prospect...</p>');

    try {
        const data = await API.post('/analyze-prospect', { prospect_id: prospectId });

        const levelColors = { Hot: 'var(--risk-high)', Warm: 'var(--risk-medium)', Cold: 'var(--accent-blue)' };

        let html = `
            <!-- ICP Score & Level -->
            <div style="display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:center;margin-bottom:24px">
                ${renderHealthGauge(data.icp_score, 110)}
                <div>
                    <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px">ICP Fit Score</div>
                    <div style="font-size:2rem;font-weight:800;color:var(--text-primary);margin:4px 0">${data.icp_score}/100</div>
                    <span class="risk-badge" style="background:${data.engagement_level === 'Hot' ? 'var(--risk-high-bg)' : data.engagement_level === 'Warm' ? 'var(--risk-medium-bg)' : 'rgba(59,130,246,0.12)'};color:${levelColors[data.engagement_level]}">${data.engagement_level === 'Hot' ? '🔥' : data.engagement_level === 'Warm' ? '☀️' : '❄️'} ${data.engagement_level}</span>
                    <span style="font-size:0.75rem;color:var(--text-muted);margin-left:8px">Priority: ${data.recommended_priority.replace('_', ' ')}</span>
                </div>
            </div>

            <!-- ICP Breakdown -->
            <h3 style="font-size:0.9rem;font-weight:700;margin-bottom:12px">📊 ICP Score Breakdown</h3>
            <div class="icp-breakdown" style="margin-bottom:24px">
                ${Object.entries(data.icp_breakdown).map(([key, val]) => `
                    <div class="icp-bar-item">
                        <span class="icp-bar-label">${key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                        <div class="icp-bar-track"><div class="icp-bar-fill" style="width:${(val.score / val.max) * 100}%"></div></div>
                        <span class="icp-bar-score">${val.score}/${val.max}</span>
                    </div>
                `).join('')}
            </div>

            <!-- AI Reasoning -->
            <div class="ai-typing-container" style="margin-bottom:24px">
                <div class="ai-typing-header">
                    <div class="ai-typing-dots"><span></span><span></span><span></span></div>
                    Prospecting Agent — Analysis
                </div>
                <div class="ai-typing-text" id="prospect-reasoning"></div>
            </div>

            <!-- 5-Touch Outreach Sequence -->
            <h3 style="font-size:0.9rem;font-weight:700;margin-bottom:16px">📬 5-Touch Outreach Sequence</h3>
            <div class="touch-sequence">
                ${data.outreach_sequence.map(t => `
                    <div class="touch-item">
                        <div class="touch-day">Day ${t.day}</div>
                        <div class="touch-channel" style="color:${t.channel === 'Email' ? 'var(--accent-blue)' : t.channel === 'WhatsApp' ? 'var(--accent-emerald)' : 'var(--accent-cyan)'}">
                            ${t.channel === 'Email' ? '📧' : t.channel === 'WhatsApp' ? '💬' : '🔗'} ${t.channel}
                        </div>
                        <div class="touch-action">${t.action}</div>
                    </div>
                `).join('')}
            </div>
        `;

        $('#modal-body').innerHTML = html;
        const reasoningEl = document.getElementById('prospect-reasoning');
        if (reasoningEl) typeText(reasoningEl, data.reasoning, 8);

    } catch (error) {
        $('#modal-body').innerHTML = `<p style="color:var(--risk-high)">Error: ${error.message}</p>`;
    }
}

async function renderRetention() {
    try {
        const data = await API.get('/customers');

        $('#content-area').innerHTML = `
            <div class="section-header">
                <div>
                    <h2 class="section-title">Revenue Retention Intelligence</h2>
                    <p class="section-subtitle">Churn prediction, MRR protection, and intervention strategies</p>
                </div>
            </div>

            <div class="content-grid">
                ${data.customers.map(c => {
                    const sentimentColor = c.sentiment === 'Positive' ? 'var(--accent-emerald)' : c.sentiment === 'Negative' ? 'var(--risk-high)' : 'var(--risk-medium)';
                    return `
                        <div class="card animate-in">
                            <div class="card-header">
                                <div>
                                    <div style="font-size:1.05rem;font-weight:700">${c.company}</div>
                                    <div style="font-size:0.8rem;color:var(--text-muted)">${c.contact_name}</div>
                                </div>
                                <span class="risk-badge" style="background:rgba(${c.sentiment === 'Negative' ? '239,68,68' : c.sentiment === 'Positive' ? '16,185,129' : '245,158,11'},0.12);color:${sentimentColor}">
                                    ${c.sentiment === 'Positive' ? '😊' : c.sentiment === 'Negative' ? '😟' : '😐'} ${c.sentiment}
                                </span>
                            </div>

                            <div style="display:flex;flex-direction:column;gap:0">
                                <div class="retention-metric">
                                    <span class="retention-metric-label">MRR</span>
                                    <span class="retention-metric-value" style="color:var(--text-primary)">${formatCurrency(c.mrr)}</span>
                                </div>
                                <div class="retention-metric">
                                    <span class="retention-metric-label">Feature Adoption</span>
                                    <span class="retention-metric-value" style="color:${c.feature_adoption < 30 ? 'var(--risk-high)' : c.feature_adoption < 60 ? 'var(--risk-medium)' : 'var(--accent-emerald)'}">${c.feature_adoption.toFixed(1)}%</span>
                                </div>
                                <div class="retention-metric">
                                    <span class="retention-metric-label">Last Login</span>
                                    <span class="retention-metric-value" style="color:${c.last_login_days_ago > 7 ? 'var(--risk-high)' : 'var(--text-primary)'}">${c.last_login_days_ago}d ago</span>
                                </div>
                                <div class="retention-metric">
                                    <span class="retention-metric-label">Support Tickets</span>
                                    <span class="retention-metric-value" style="color:${c.support_tickets > 3 ? 'var(--risk-high)' : 'var(--text-primary)'}">${c.support_tickets}</span>
                                </div>
                                <div class="retention-metric">
                                    <span class="retention-metric-label">Contract Ends</span>
                                    <span class="retention-metric-value">${c.contract_end_date}</span>
                                </div>
                            </div>

                            <button class="btn btn-primary btn-sm" style="width:100%;margin-top:16px" onclick="analyzeRetention('${c.id}')">🤖 Run Churn Analysis</button>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error: ${error.message}</p></div>`;
    }
}

async function analyzeRetention(customerId) {
    openModal('Revenue Retention Analysis', '<div class="spinner"></div><p style="text-align:center;color:var(--text-muted);margin-top:12px">Analyzing churn risk...</p>');

    try {
        const data = await API.post('/retention-analysis', { customer_id: customerId });

        const churnColor = data.churn_probability >= 70 ? 'var(--risk-high)' : data.churn_probability >= 40 ? 'var(--risk-medium)' : 'var(--accent-emerald)';

        let html = `
            <!-- Churn Score -->
            <div style="display:grid;grid-template-columns:auto 1fr;gap:24px;align-items:center;margin-bottom:24px">
                ${renderHealthGauge(100 - data.churn_probability, 110)}
                <div>
                    <div style="font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px">Churn Probability</div>
                    <div style="font-size:2.2rem;font-weight:800;color:${churnColor};margin:4px 0">${data.churn_probability}%</div>
                    <span class="risk-badge ${getRiskClass(data.churn_probability)}">${data.churn_level} Risk</span>
                </div>
            </div>

            <!-- MRR Impact -->
            <div class="revenue-impact" style="margin-bottom:24px;background:linear-gradient(135deg, rgba(239,68,68,0.06), rgba(245,158,11,0.06));border-color:rgba(239,68,68,0.15)">
                <div class="saved-label" style="color:var(--risk-high)">⚠️ MRR at Risk</div>
                <div class="saved-value" style="background:var(--gradient-danger);-webkit-background-clip:text">${formatCurrency(data.mrr_at_risk)}/month</div>
                <div class="saved-detail">Annual impact: ${formatCurrency(data.annual_revenue_at_risk)}</div>
                ${data.days_to_renewal <= 60 ? `<p style="font-size:0.8rem;font-weight:600;color:var(--risk-high);margin-top:8px">⏰ Contract renewal in ${data.days_to_renewal} days!</p>` : ''}
            </div>

            <!-- Churn Factors -->
            ${data.churn_factors.length > 0 ? `
                <h3 style="font-size:0.9rem;font-weight:700;margin-bottom:12px">⚠️ Churn Risk Factors</h3>
                ${data.churn_factors.map(cf => `
                    <div class="risk-factor-item ${cf.severity}">
                        <div style="flex:1">
                            <div class="risk-factor-name">${cf.factor}</div>
                            <div class="risk-factor-detail">${cf.detail}</div>
                        </div>
                        <span class="risk-factor-impact" style="background:${cf.severity === 'critical' ? 'var(--risk-high-bg)' : 'var(--risk-medium-bg)'};color:${cf.severity === 'critical' ? 'var(--risk-high)' : 'var(--risk-medium)'}">+${cf.impact}</span>
                    </div>
                `).join('')}
            ` : ''}

            ${data.positive_signals.length > 0 ? `
                <h3 style="font-size:0.9rem;font-weight:700;margin:20px 0 12px">✅ Positive Signals</h3>
                <ul style="list-style:none;padding:0">
                    ${data.positive_signals.map(ps => `<li style="padding:6px 0;font-size:0.83rem;color:var(--accent-emerald)">✓ ${ps}</li>`).join('')}
                </ul>
            ` : ''}

            <!-- AI Reasoning -->
            <div class="ai-typing-container" style="margin:20px 0">
                <div class="ai-typing-header">
                    <div class="ai-typing-dots"><span></span><span></span><span></span></div>
                    Revenue Retention Agent — Analysis
                </div>
                <div class="ai-typing-text" id="retention-reasoning"></div>
            </div>

            <!-- Intervention Plan -->
            <h3 style="font-size:0.9rem;font-weight:700;margin:24px 0 12px">🛡️ Intervention Plan (${data.intervention_plan.urgency.toUpperCase()})</h3>
            <p style="font-size:0.75rem;color:var(--text-muted);margin-bottom:16px">Timeline: ${data.intervention_plan.timeline}</p>
            ${data.intervention_plan.actions.map((a, i) => `
                <div class="intervention-step">
                    <div class="intervention-number">${i + 1}</div>
                    <div class="intervention-content">
                        <div class="intervention-action">${a.action}</div>
                        <div class="intervention-detail">${a.detail}</div>
                        <div class="intervention-meta">
                            <span>👤 ${a.owner}</span>
                            <span>⏰ ${a.deadline}</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        `;

        $('#modal-body').innerHTML = html;
        const reasoningEl = document.getElementById('retention-reasoning');
        if (reasoningEl) typeText(reasoningEl, data.reasoning, 8);

    } catch (error) {
        $('#modal-body').innerHTML = `<p style="color:var(--risk-high)">Error: ${error.message}</p>`;
    }
}

async function renderCompetitive() {
    try {
        const data = await API.get('/deals');
        const deals = data.deals.filter(d => d.stage !== 'Closed Won' && d.stage !== 'Closed Lost');

        $('#content-area').innerHTML = `
            <div class="section-header">
                <div>
                    <h2 class="section-title">Competitive Intelligence</h2>
                    <p class="section-subtitle">Battlecards, objection handlers, and positioning strategies</p>
                </div>
            </div>

            <div class="content-grid">
                ${deals.map(d => `
                    <div class="card animate-in" style="cursor:pointer" onclick="analyzeCompetitive('${d.id}')">
                        <div class="card-header">
                            <div>
                                <div style="font-size:1.05rem;font-weight:700">${d.company}</div>
                                <div style="font-size:0.8rem;color:var(--text-muted)">${d.industry || 'General'} · ${d.stage}</div>
                            </div>
                            <div class="card-icon amber">⚔️</div>
                        </div>
                        <p style="font-size:0.83rem;color:var(--text-secondary);margin-bottom:12px">Deal: ${formatCurrency(d.deal_value)}</p>
                        <button class="btn btn-primary btn-sm" style="width:100%">🏴 Generate Battlecard</button>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error: ${error.message}</p></div>`;
    }
}

async function analyzeCompetitive(dealId) {
    openModal('Competitive Intelligence', '<div class="spinner"></div><p style="text-align:center;color:var(--text-muted);margin-top:12px">Generating competitive analysis...</p>');

    try {
        const data = await API.post('/competitive-analysis', { deal_id: dealId });

        let html = `
            <!-- Positioning Strategy -->
            <div class="positioning-card" style="margin-bottom:24px">
                <div class="positioning-headline">${data.positioning.headline}</div>
                <div class="positioning-vp">${data.positioning.value_proposition}</div>
                <div class="proof-points">
                    ${data.positioning.proof_points.map(pp => `
                        <div class="proof-point">
                            <div class="proof-point-metric">${pp.metric}</div>
                            <div class="proof-point-desc">${pp.description}</div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- Battlecards -->
            <h3 style="font-size:0.95rem;font-weight:700;margin-bottom:16px">🏴 Battlecards</h3>
            ${data.battlecards.map(bc => `
                <div class="battlecard">
                    <div class="battlecard-header">
                        <div class="battlecard-title">vs. ${bc.competitor}</div>
                        <span class="risk-badge medium">⚔️ Competitor</span>
                    </div>
                    <div class="battlecard-body">
                        <div class="battlecard-section">
                            <div class="battlecard-section-title">Key Differentiators</div>
                            <ul class="battlecard-list">
                                ${bc.key_differentiators.map(d => `<li>${d}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="battlecard-section">
                            <div class="battlecard-section-title">Win Strategy</div>
                            <p style="font-size:0.83rem;color:var(--text-secondary);line-height:1.6">${bc.win_strategy}</p>
                        </div>
                        <div class="battlecard-section">
                            <div class="battlecard-section-title">Counter Narrative</div>
                            <p style="font-size:0.83rem;color:var(--accent-emerald);line-height:1.6;font-style:italic">"${bc.counter_narrative}"</p>
                        </div>
                    </div>
                </div>
            `).join('')}

            <!-- Objection Handlers -->
            <h3 style="font-size:0.95rem;font-weight:700;margin:24px 0 16px">🛡️ Objection Handlers</h3>
            ${data.objection_handlers.map(oh => `
                <div class="objection-card">
                    <div class="objection-question">❓ "${oh.objection}"</div>
                    <div class="objection-answer">${oh.response}</div>
                    <div class="objection-proof">💡 ${oh.proof}</div>
                    <div style="font-size:0.7rem;color:var(--text-muted);margin-top:6px">Approach: ${oh.approach}</div>
                </div>
            `).join('')}

            <!-- AI Reasoning -->
            <div class="ai-typing-container" style="margin-top:20px">
                <div class="ai-typing-header">
                    <div class="ai-typing-dots"><span></span><span></span><span></span></div>
                    Competitive Intelligence Agent — Analysis
                </div>
                <div class="ai-typing-text" id="competitive-reasoning"></div>
            </div>
        `;

        $('#modal-body').innerHTML = html;
        const reasoningEl = document.getElementById('competitive-reasoning');
        if (reasoningEl) typeText(reasoningEl, data.reasoning, 8);

    } catch (error) {
        $('#modal-body').innerHTML = `<p style="color:var(--risk-high)">Error: ${error.message}</p>`;
    }
}

async function renderAudit() {
    try {
        const data = await API.get('/audit-logs');

        $('#content-area').innerHTML = `
            <div class="section-header">
                <div>
                    <h2 class="section-title">AI Decision Audit Trail</h2>
                    <p class="section-subtitle">Complete log of all AI agent decisions and actions</p>
                </div>
            </div>

            <div class="card animate-in">
                ${data.logs.length > 0 ? `
                    ${data.logs.map(log => `
                        <div class="audit-entry">
                            <div class="audit-time">${new Date(log.timestamp).toLocaleTimeString('en-IN', {hour: '2-digit', minute: '2-digit'})}</div>
                            <div class="audit-agent">${log.agent_name}</div>
                            <div class="audit-content">
                                <div class="audit-action">${log.action}</div>
                                <div class="audit-detail">${log.input_summary} → ${log.output_summary}</div>
                            </div>
                        </div>
                    `).join('')}
                ` : '<div class="empty-state"><div class="empty-state-icon">📋</div><p class="empty-state-text">No audit logs yet. Run an AI analysis to generate entries.</p></div>'}
            </div>
        `;
    } catch (error) {
        $('#content-area').innerHTML = `<div class="card"><p style="color:var(--risk-high)">Error: ${error.message}</p></div>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const page = location.hash.slice(1) || 'dashboard';
    navigate(page);
});

// Make functions globally accessible
window.analyzeDeal = analyzeDeal;
window.analyzeProspect = analyzeProspect;
window.analyzeRetention = analyzeRetention;
window.analyzeCompetitive = analyzeCompetitive;
window.runPipelineAnalysis = runPipelineAnalysis;
