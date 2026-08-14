from __future__ import annotations

import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from core.scenario import ACTION_CODES, all_selections, marginal_effects, selection_label, simulate


ROOT = Path(__file__).parent
SNAPSHOT_PATH = ROOT / "data" / "final_snapshot.json"

NAVY = "#0B1020"
PANEL = "#141B2D"
PANEL_2 = "#1B2338"
TEXT = "#F3F5FA"
MUTED = "#A8B0C2"
MINT = "#55D6B1"
MAGENTA = "#F05A89"
AMBER = "#F2B84B"
PURPLE = "#8B6CF0"
GRID = "#34405A"


st.set_page_config(
    page_title="NovaCorp Decision Lab",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_snapshot() -> dict:
    return json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))


def money(value: float, decimals: int = 1) -> str:
    sign = "−" if value < 0 else ""
    return f"{sign}A${abs(value):,.{decimals}f}M"


def number(value: float, decimals: int = 0) -> str:
    return f"{value:,.{decimals}f}"


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&display=swap');
        :root {
          --nc-bg:#0B1020; --nc-panel:#141B2D; --nc-panel2:#1B2338;
          --nc-text:#F3F5FA; --nc-muted:#A8B0C2; --nc-mint:#55D6B1;
          --nc-pink:#F05A89; --nc-amber:#F2B84B; --nc-purple:#8B6CF0;
          --nc-border:#2B3650;
        }
        html, body, [class*="css"], .stApp {font-family:'Archivo','Segoe UI',sans-serif;}
        .stApp {
          background:
            radial-gradient(circle at 85% 5%, rgba(139,108,240,.13), transparent 28rem),
            radial-gradient(circle at 15% 15%, rgba(85,214,177,.07), transparent 24rem),
            var(--nc-bg);
          color:var(--nc-text);
        }
        .block-container {max-width:1280px; padding-top:2rem; padding-bottom:4rem;}
        [data-testid="stSidebar"] {background:#0E1424; border-right:1px solid var(--nc-border);}
        [data-testid="stSidebar"] * {color:var(--nc-text);}
        h1,h2,h3 {letter-spacing:-.025em; color:var(--nc-text)!important;}
        h1 {font-size:2.35rem!important; margin-bottom:.35rem!important;}
        h2 {font-size:1.45rem!important; margin-top:1.7rem!important;}
        h3 {font-size:1.05rem!important;}
        p, li, label, .stMarkdown {color:var(--nc-text);}
        div[data-testid="stCaptionContainer"] p {color:var(--nc-muted)!important;}
        .nc-kicker {color:var(--nc-mint); font-size:.78rem; font-weight:700; letter-spacing:.15em; text-transform:uppercase; margin-bottom:.4rem;}
        .nc-lead {color:var(--nc-muted); font-size:1.03rem; max-width:900px; margin-bottom:1.25rem;}
        .nc-hero {
          background:linear-gradient(125deg, rgba(139,108,240,.17), rgba(85,214,177,.06));
          border:1px solid var(--nc-border); border-radius:20px; padding:1.4rem 1.55rem; margin:.75rem 0 1.2rem;
        }
        .nc-hero strong {color:var(--nc-mint);}
        .nc-grid {display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:.8rem; margin:.6rem 0 1rem;}
        .nc-kpi {background:rgba(20,27,45,.93); border:1px solid var(--nc-border); border-radius:16px; padding:1rem 1.05rem; min-height:112px;}
        .nc-kpi-label {color:var(--nc-muted); font-size:.78rem; text-transform:uppercase; letter-spacing:.07em; font-weight:700;}
        .nc-kpi-value {color:var(--nc-text); font-size:1.75rem; font-weight:700; margin:.28rem 0 .18rem;}
        .nc-kpi-note {color:var(--nc-muted); font-size:.82rem;}
        .nc-card {background:rgba(20,27,45,.94); border:1px solid var(--nc-border); border-radius:17px; padding:1.05rem 1.1rem; margin-bottom:.55rem; height:100%;}
        .nc-card.selected {border-color:var(--nc-mint); box-shadow:0 0 0 1px rgba(85,214,177,.22), 0 12px 32px rgba(0,0,0,.18);}
        .nc-card.rejected {border-color:rgba(240,90,137,.45); background:rgba(75,28,48,.28);}
        .nc-card-title {font-size:1.02rem; font-weight:700; margin:.35rem 0 .45rem; color:var(--nc-text);}
        .nc-card-copy {color:var(--nc-muted); font-size:.88rem; min-height:3.4rem;}
        .nc-card-action {font-size:.86rem; color:var(--nc-text); border-top:1px solid var(--nc-border); padding-top:.65rem; margin-top:.7rem; min-height:3.4rem;}
        .nc-facts {display:grid; grid-template-columns:repeat(3,1fr); gap:.42rem; margin-top:.75rem;}
        .nc-fact {background:var(--nc-panel2); border-radius:10px; padding:.55rem .5rem;}
        .nc-fact span {display:block; color:var(--nc-muted); font-size:.68rem; text-transform:uppercase; letter-spacing:.04em;}
        .nc-fact b {display:block; color:var(--nc-text); font-size:.93rem; margin-top:.12rem;}
        .nc-badge {display:inline-block; border-radius:999px; padding:.23rem .55rem; font-size:.68rem; font-weight:700; letter-spacing:.06em; text-transform:uppercase;}
        .nc-badge-evidence {background:rgba(85,214,177,.14); color:var(--nc-mint);}
        .nc-badge-assumption {background:rgba(242,184,75,.14); color:var(--nc-amber);}
        .nc-badge-scenario {background:rgba(139,108,240,.17); color:#B9A9FF;}
        .nc-badge-reject {background:rgba(240,90,137,.15); color:#FF8CAF;}
        .nc-compare {display:grid; grid-template-columns:1fr auto 1fr; gap:.75rem; align-items:stretch; margin:.8rem 0 1rem;}
        .nc-compare-side {background:var(--nc-panel); border:1px solid var(--nc-border); border-radius:18px; padding:1.2rem;}
        .nc-compare-side.action {border-color:rgba(85,214,177,.65); background:linear-gradient(145deg, rgba(85,214,177,.12), rgba(20,27,45,.96));}
        .nc-compare-label {color:var(--nc-muted); font-size:.75rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase;}
        .nc-compare-value {font-size:2rem; font-weight:700; color:var(--nc-text); margin:.3rem 0;}
        .nc-compare-arrow {align-self:center; color:var(--nc-mint); font-size:1.7rem;}
        .nc-summary {background:linear-gradient(120deg,rgba(85,214,177,.13),rgba(139,108,240,.12)); border:1px solid rgba(85,214,177,.45); border-radius:16px; padding:1rem 1.15rem; color:var(--nc-text); margin:.75rem 0;}
        .nc-warning {background:rgba(242,184,75,.09); border-left:3px solid var(--nc-amber); padding:.85rem 1rem; border-radius:8px; color:var(--nc-text); margin:.65rem 0;}
        .nc-danger {background:rgba(240,90,137,.09); border-left:3px solid var(--nc-pink); padding:.85rem 1rem; border-radius:8px; color:var(--nc-text); margin:.65rem 0;}
        .nc-row {display:flex; gap:.55rem; flex-wrap:wrap; align-items:center;}
        .nc-mini {background:var(--nc-panel2); border-radius:12px; padding:.65rem .75rem; flex:1; min-width:135px;}
        .nc-mini span {color:var(--nc-muted); display:block; font-size:.7rem; text-transform:uppercase;}
        .nc-mini b {color:var(--nc-text); display:block; margin-top:.15rem;}
        .nc-evidence {background:var(--nc-panel); border:1px solid var(--nc-border); border-radius:16px; padding:1rem; margin-bottom:.8rem; min-height:230px;}
        .nc-evidence h4 {color:var(--nc-text); margin:.5rem 0 .6rem; font-size:1rem;}
        .nc-evidence dt {color:var(--nc-muted); font-size:.7rem; text-transform:uppercase; letter-spacing:.06em; font-weight:700; margin-top:.55rem;}
        .nc-evidence dd {color:var(--nc-text); font-size:.87rem; margin:.15rem 0 0;}
        .nc-step {display:grid; grid-template-columns:36px 1fr; gap:.75rem; margin:.8rem 0; align-items:start;}
        .nc-step-num {width:34px; height:34px; border-radius:50%; background:rgba(139,108,240,.2); color:#C7B9FF; display:flex; align-items:center; justify-content:center; font-weight:700;}
        .nc-step-copy b {color:var(--nc-text);}
        .nc-step-copy span {display:block; color:var(--nc-muted); margin-top:.2rem;}
        .nc-table {width:100%; border-collapse:collapse; margin:.65rem 0; color:var(--nc-text); font-size:.86rem;}
        .nc-table th {text-align:left; color:var(--nc-muted); font-size:.7rem; text-transform:uppercase; letter-spacing:.05em; border-bottom:1px solid var(--nc-border); padding:.55rem;}
        .nc-table td {border-bottom:1px solid var(--nc-border); padding:.65rem .55rem; vertical-align:top;}
        .nc-positive {color:var(--nc-mint)!important;} .nc-negative {color:#FF8CAF!important;} .nc-amber {color:var(--nc-amber)!important;}
        [data-testid="stMetric"] {background:var(--nc-panel); border:1px solid var(--nc-border); padding:.9rem 1rem; border-radius:14px;}
        [data-testid="stMetricLabel"] p {color:var(--nc-muted)!important;}
        [data-testid="stMetricValue"] {color:var(--nc-text)!important;}
        [data-testid="stTabs"] button {color:var(--nc-muted);}
        [data-testid="stTabs"] button[aria-selected="true"] {color:var(--nc-mint);}
        [data-testid="stExpander"] {background:rgba(20,27,45,.65); border:1px solid var(--nc-border); border-radius:13px;}
        .stButton > button {border-radius:10px; border-color:var(--nc-border);}
        .stToggle label p {font-weight:600;}
        @media (max-width:760px) {
          .block-container {padding-left:1rem; padding-right:1rem;}
          .nc-compare {grid-template-columns:1fr;}
          .nc-compare-arrow {transform:rotate(90deg); text-align:center;}
          .nc-facts {grid-template-columns:1fr 1fr;}
          h1 {font-size:1.85rem!important;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_title(kicker: str, heading: str, lead: str) -> None:
    st.markdown(f'<div class="nc-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.title(heading)
    st.markdown(f'<div class="nc-lead">{lead}</div>', unsafe_allow_html=True)


def kpi_grid(items: list[tuple[str, str, str]]) -> None:
    html = '<div class="nc-grid">'
    for label, value, note in items:
        html += f'<div class="nc-kpi"><div class="nc-kpi-label">{label}</div><div class="nc-kpi-value">{value}</div><div class="nc-kpi-note">{note}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def altair_theme(chart: alt.Chart) -> alt.Chart:
    return chart.configure(
        background="transparent",
        font="Archivo",
    ).configure_axis(
        labelColor=MUTED,
        titleColor=MUTED,
        gridColor=GRID,
        domainColor=GRID,
        tickColor=GRID,
        labelFontSize=12,
        titleFontSize=12,
    ).configure_view(strokeOpacity=0).configure_legend(
        labelColor=MUTED,
        titleColor=MUTED,
    ).configure_title(color=TEXT, anchor="start", fontSize=16, fontWeight=600)


def story_card(title: str, value: str, copy: str, badge: str, badge_class: str) -> str:
    return f"""
    <div class="nc-card">
      <span class="nc-badge {badge_class}">{badge}</span>
      <div class="nc-card-title">{title}</div>
      <div class="nc-kpi-value">{value}</div>
      <div class="nc-card-copy">{copy}</div>
    </div>
    """


def overview_page(data: dict) -> None:
    finance = data["finance"]
    workforce = data["workforce"]
    measurement = data["measurement"]
    warning = data["warning"]
    drivers = data["drivers"]

    page_title(
        "Executive decision view",
        "See the loss correctly. Act only where there is a mechanism.",
        "NovaCorp’s problem is preventable high-value loss combined with incomplete detection—not one undifferentiated attrition rate.",
    )
    st.markdown(
        f"""
        <div class="nc-hero">
          Finance reported approximately <strong>{money(finance['reported_total_m'],0)}</strong> in annual people cost.
          Rebuilding the three buckets produces <strong>{money(finance['rebuilt_total_m'])}</strong>, but only the
          <strong>{money(finance['regrettable_m'])}</strong> regrettable-attrition bucket is both strongly reconciled and central to this retention strategy.
        </div>
        """,
        unsafe_allow_html=True,
    )

    kpi_grid(
        [
            ("Genuine regrettable attrition", money(finance["regrettable_m"]), f"{finance['genuine_exits_2y']} exits over 24 months"),
            ("Invisible to the current flag", money(measurement["missed_m"]), f"{measurement['fn']} target exits missed"),
            ("Inside three bounded drivers", money(drivers["union_cost_m"]), f"{drivers['union_share_pct']:.0f}% of annual exposure, de-duplicated"),
        ]
    )

    st.markdown("## The decision story")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            story_card(
                "1 · Separate push from pull",
                f"{100*workforce['push']/workforce['voluntary']:.0f}%",
                f"{workforce['push']} of {workforce['voluntary']} recorded voluntary exits were managed-out push exits. Retention should focus on employee-initiated pull loss.",
                "Validated evidence",
                "nc-badge-evidence",
            ),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            story_card(
                "2 · Fix what HR can see",
                f"{measurement['recall_pct']:.1f}%",
                f"The old flag caught {measurement['tp']} of {finance['genuine_exits_2y']} target exits. The new three-field definition raises annual case review from about {measurement['old_reviews_pa']:.0f} to {measurement['new_reviews_pa']:.0f}.",
                "Measurement",
                "nc-badge-evidence",
            ),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            story_card(
                "3 · Do not chase warning signals",
                f"{warning['headline_pct']:.0f}%",
                f"Target leavers still answered their final survey; their last score was only {warning['headline_last_z']:.2f}z below average (p={warning['p_value']:.2f}) with no meaningful own-score decline.",
                "Boundary",
                "nc-badge-assumption",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("## Three drivers become three testable moves")
    intervention = {row["code"]: row for row in data["interventions"]}
    historical = {row["code"]: row for row in drivers["historical"]}
    cols = st.columns(3)
    for col, code, accent in zip(cols, ACTION_CODES, [MINT, MAGENTA, AMBER]):
        item = intervention[code]
        hist = historical[code]
        with col:
            st.markdown(
                f"""
                <div class="nc-card" style="border-top:3px solid {accent}">
                  <span class="nc-badge nc-badge-evidence">Driver {code}</span>
                  <div class="nc-card-title">{item['short_name']}</div>
                  <div class="nc-card-copy">{item['problem']}</div>
                  <div class="nc-facts">
                    <div class="nc-fact"><span>Historical</span><b>{money(hist['cost_m'])}</b></div>
                    <div class="nc-fact"><span>2026 reachable</span><b>{money(item['addressable_m'])}</b></div>
                    <div class="nc-fact"><span>Break-even</span><b>{item['break_even_pct']:.0f}%</b></div>
                  </div>
                  <div class="nc-card-action"><b>Move:</b> {item['action']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div class="nc-warning"><b>Do not add the three historical bars.</b> The cohorts overlap. Their de-duplicated union is {money(drivers['union_cost_m'])}; the remaining {money(drivers['residual_cost_m'])} across {drivers['residual_exits_2y']} exits has no shared observed mechanism and receives no generic programme.</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Recommended operating sequence")
    st.markdown(
        """
        <div class="nc-step"><div class="nc-step-num">1</div><div class="nc-step-copy"><b>Fix measurement now</b><span>Use voluntary + employee-initiated pull + top-two performance or HiPo. This improves visibility; it is not an employee prediction model.</span></div></div>
        <div class="nc-step"><div class="nc-step-num">2</div><div class="nc-step-copy"><b>Pilot C, D and E as separate accountable programmes</b><span>Each has a mechanism, owner, cost and break-even hurdle. Do not fund blanket pay or blanket promotion.</span></div></div>
        <div class="nc-step"><div class="nc-step-num">3</div><div class="nc-step-copy"><b>Measure before scaling</b><span>Use a phased or randomized comparison, 365-day exits, operational delivery, net cost and fairness stopping conditions.</span></div></div>
        """,
        unsafe_allow_html=True,
    )


def reset_scenario(data: dict) -> None:
    st.session_state["action_C"] = True
    st.session_state["action_D"] = True
    st.session_state["action_E"] = True
    st.session_state["efficacy_preset"] = "Notebook prior · 30.4%"
    st.session_state["custom_efficacy"] = 30
    st.session_state["pulse_exits"] = float(data["scenario"]["entity_pulse_exits"])
    interventions = {row["code"]: row for row in data["interventions"]}
    for code in ACTION_CODES:
        st.session_state[f"cost_{code}"] = float(interventions[code]["cost_m"])


def strategy_card(item: dict, selected: bool) -> str:
    state_class = " selected" if selected else ""
    return f"""
    <div class="nc-card{state_class}">
      <span class="nc-badge nc-badge-scenario">{item['code']} · {item['status']}</span>
      <div class="nc-card-title">{item['short_name']}</div>
      <div class="nc-card-copy">{item['problem']}</div>
      <div class="nc-facts">
        <div class="nc-fact"><span>Cost</span><b>{money(item['cost_m'])}</b></div>
        <div class="nc-fact"><span>Reachable</span><b>{money(item['addressable_m'])}</b></div>
        <div class="nc-fact"><span>Break-even</span><b>{item['break_even_pct']:.0f}%</b></div>
      </div>
      <div class="nc-card-action"><b>Action:</b> {item['action']}</div>
    </div>
    """


@st.cache_data(show_spinner=False)
def combination_results(efficacy: float, pulse: float, cost_c: float, cost_d: float, cost_e: float) -> pd.DataFrame:
    data = load_snapshot()
    rows = []
    for index, selected in enumerate(all_selections()):
        result = simulate(
            data,
            selected,
            efficacy,
            pulse_exits=pulse,
            costs={"C": cost_c, "D": cost_d, "E": cost_e},
            n=10_000,
            seed=42,
        )
        strategy = result.selection
        reference = data["scenario"]["reference"]
        interventions = {row["code"]: row for row in data["interventions"]}
        default_inputs = (
            abs(efficacy - data["scenario"]["efficacy_mean_pct"] / 100) < 1e-9
            and abs(pulse - data["scenario"]["entity_pulse_exits"]) < 1e-6
            and abs(cost_c - interventions["C"]["cost_m"]) < 1e-6
            and abs(cost_d - interventions["D"]["cost_m"]) < 1e-6
            and abs(cost_e - interventions["E"]["cost_m"]) < 1e-6
        )
        locked = reference.get(strategy) if default_inputs else None
        rows.append(
            {
                "strategy": strategy,
                "p05": locked["p05_m"] if locked else result.scenario_p05_m,
                "median": locked["median_m"] if locked else result.scenario_median_m,
                "p95": locked["p95_m"] if locked else result.scenario_p95_m,
                "expected_net": result.expected_net_value_m,
                "probability_lower": locked["probability_lower_pct"] if locked else result.probability_lower_pct,
            }
        )
    return pd.DataFrame(rows)


def scenario_page(data: dict) -> None:
    scenario = data["scenario"]
    interventions = {row["code"]: row for row in data["interventions"]}

    page_title(
        "Interactive strategy simulator",
        "Choose a move. See the financial consequence immediately.",
        "Start from the finalized 2026 baseline, switch individual programmes on or off, and test how much efficacy each portfolio needs before it becomes financially plausible.",
    )

    if "action_C" not in st.session_state:
        reset_scenario(data)

    top_a, top_b = st.columns([1, 4])
    with top_a:
        st.button("Reset to notebook", on_click=reset_scenario, args=(data,), width="stretch")
    with top_b:
        st.markdown(
            f'<div class="nc-warning"><b>How to use:</b> select C, D and/or E; choose an efficacy assumption; compare “do nothing” with the selected portfolio. The default reproduces the notebook’s C+D+E decision case.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("## 1 · Select the moves")
    columns = st.columns(3)
    selected: set[str] = set()
    for column, code in zip(columns, ACTION_CODES):
        with column:
            is_on = bool(st.session_state.get(f"action_{code}", True))
            st.markdown(strategy_card(interventions[code], is_on), unsafe_allow_html=True)
            enabled = st.toggle(f"Include {code} · {interventions[code]['short_name']}", key=f"action_{code}")
            if enabled:
                selected.add(code)

    with st.expander("Why broad options A and B were rejected"):
        rejected = {row["code"]: row for row in data["interventions"] if row["code"] in {"A", "B"}}
        st.markdown(
            f"""
            <table class="nc-table">
              <thead><tr><th>Option</th><th>Annual cost</th><th>Reachable exposure</th><th>Break-even</th><th>Decision</th></tr></thead>
              <tbody>
                <tr><td><b>A · Blanket HiPo pay</b></td><td>{money(rejected['A']['cost_m'])}</td><td>{money(rejected['A']['addressable_m'])}</td><td class="nc-negative">{rejected['A']['break_even_pct']:.0f}%</td><td>Impossible even at 100% efficacy</td></tr>
                <tr><td><b>B · Blanket promotion</b></td><td>{money(rejected['B']['cost_m'])}</td><td>27% of {money(rejected['B']['addressable_m'])}</td><td class="nc-negative">{rejected['B']['break_even_pct']:.0f}%</td><td>Most spend is outside reachable exposure</td></tr>
              </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## 2 · Choose how well the pilot works")
    preset = st.radio(
        "Share of reachable exits prevented",
        ["Conservative · 15%", "Notebook prior · 30.4%", "Strong · 45%", "Custom"],
        key="efficacy_preset",
        horizontal=True,
        help="This is not a reduction in NovaCorp-wide attrition. It is the share of exits reachable by each selected programme that are prevented.",
    )
    if preset.startswith("Conservative"):
        efficacy = 0.15
    elif preset.startswith("Notebook"):
        efficacy = scenario["efficacy_mean_pct"] / 100
    elif preset.startswith("Strong"):
        efficacy = 0.45
    else:
        efficacy = st.slider(
            "Custom efficacy",
            min_value=0,
            max_value=60,
            step=1,
            format="%d%%",
            key="custom_efficacy",
        ) / 100

    with st.expander("Advanced planning assumptions"):
        st.caption("Changing these values creates a derived scenario. It does not change the finalized historical evidence.")
        pulse = st.number_input(
            "Expected additional consolidation exits",
            min_value=0.0,
            max_value=40.0,
            step=1.0,
            key="pulse_exits",
            help="The finalized notebook assumes approximately 16 incremental exits above the Entity B/C steady-state baseline.",
        )
        cost_columns = st.columns(3)
        costs = {}
        for column, code in zip(cost_columns, ACTION_CODES):
            with column:
                costs[code] = st.number_input(
                    f"{code} annual programme cost (A$M)",
                    min_value=0.0,
                    max_value=20.0,
                    step=0.1,
                    key=f"cost_{code}",
                )
    if "pulse" not in locals():
        pulse = float(st.session_state.get("pulse_exits", scenario["entity_pulse_exits"]))
        costs = {code: float(st.session_state.get(f"cost_{code}", interventions[code]["cost_m"])) for code in ACTION_CODES}

    result = simulate(data, selected, efficacy, pulse_exits=pulse, costs=costs, n=10_000, seed=42)
    default_inputs = (
        abs(efficacy - scenario["efficacy_mean_pct"] / 100) < 1e-9
        and abs(pulse - scenario["entity_pulse_exits"]) < 1e-6
        and all(abs(costs[c] - interventions[c]["cost_m"]) < 1e-6 for c in ACTION_CODES)
    )
    key = selection_label(selected)
    reference_available = default_inputs and key in scenario["reference"]
    if reference_available:
        reference = scenario["reference"][key]
        display_p05 = reference["p05_m"]
        display_median = reference["median_m"]
        display_p95 = reference["p95_m"]
        display_difference = reference["difference_m"]
        display_probability = reference["probability_lower_pct"]
        source_badge = '<span class="nc-badge nc-badge-evidence">Final notebook output</span>'
    else:
        display_p05 = result.scenario_p05_m
        display_median = result.scenario_median_m
        display_p95 = result.scenario_p95_m
        display_difference = result.median_difference_m
        display_probability = result.probability_lower_pct
        source_badge = '<span class="nc-badge nc-badge-scenario">Derived scenario output</span>'

    st.markdown("## 3 · Compare doing nothing with the selected strategy")
    st.markdown(source_badge, unsafe_allow_html=True)
    direction = "lower" if display_difference < 0 else "higher"
    difference_class = "nc-positive" if display_difference < 0 else "nc-negative"
    action_name = key.replace("+", " + ") if key != "NONE" else "No programme selected"
    st.markdown(
        f"""
        <div class="nc-compare">
          <div class="nc-compare-side">
            <div class="nc-compare-label">Do nothing</div>
            <div class="nc-compare-value">{money(scenario['reference']['NONE']['median_m'])}</div>
            <div class="nc-card-copy">Median 2026 headline-attrition cost<br>{scenario['expected_exits']:.0f} expected exits · 90% range {money(scenario['reference']['NONE']['p05_m'])}–{money(scenario['reference']['NONE']['p95_m'])}</div>
          </div>
          <div class="nc-compare-arrow">→</div>
          <div class="nc-compare-side action">
            <div class="nc-compare-label">Take action · {action_name}</div>
            <div class="nc-compare-value">{money(display_median)}</div>
            <div class="nc-card-copy"><span class="{difference_class}"><b>{money(abs(display_difference))} {direction}</b></span> than status quo median<br>{result.expected_avoided_exits:.1f} expected avoided exits · 90% range {money(display_p05)}–{money(display_p95)}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if selected:
        probability_text = f"{display_probability:.1f}%" if display_probability is not None else "—"
        kpi_grid(
            [
                ("Expected avoided exits", number(result.expected_avoided_exits, 1), f"{result.expected_exits_after:.0f} expected exits remain"),
                ("Gross exposure avoided", money(result.gross_avoided_m), f"at {100*efficacy:.1f}% efficacy"),
                ("Programme spend", money(result.programme_cost_m), action_name),
                ("Expected net value", money(result.expected_net_value_m), "gross avoided exposure minus spend"),
                ("Portfolio break-even", f"{result.break_even_pct:.1f}%", "minimum common efficacy under these inputs"),
                ("Probability cost is lower", probability_text, "under the model assumptions"),
            ]
        )

        verdict = (
            "Financially plausible — pilot and measure before scaling."
            if efficacy * 100 >= (result.break_even_pct or 999)
            else "Below break-even under these assumptions — do not scale."
        )
        verdict_class = "nc-summary" if efficacy * 100 >= (result.break_even_pct or 999) else "nc-danger"
        st.markdown(
            f"""
            <div class="{verdict_class}"><b>{verdict}</b><br>
            At {100*efficacy:.1f}% efficacy, {action_name} addresses {money(result.gross_avoided_m)} of replacement exposure and costs {money(result.programme_cost_m)}, producing {money(result.expected_net_value_m)} expected net value. This is a conditional planning result—not a guarantee that the interventions cause retention.</div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="nc-danger"><b>No intervention selected.</b> This is the status quo. Switch on C, D or E above to see the incremental effect.</div>', unsafe_allow_html=True)

    if selected:
        st.markdown("### What each move contributes at this efficacy")
        marginal = marginal_effects(data, efficacy, pulse, costs)
        rows = ""
        for row in marginal:
            selected_mark = "✓ Selected" if row["code"] in selected else "Not selected"
            net_class = "nc-positive" if row["net_m"] >= 0 else "nc-negative"
            rows += f"""
            <tr>
              <td><b>{row['code']} · {row['name']}</b><br><span style="color:{MUTED}">{selected_mark}</span></td>
              <td>{row['expected_avoided_exits']:.1f}</td>
              <td>{money(row['gross_avoided_m'])}</td>
              <td>{money(row['cost_m'])}</td>
              <td class="{net_class}"><b>{money(row['net_m'])}</b></td>
              <td>{row['break_even_pct']:.0f}%</td>
            </tr>
            """
        st.markdown(
            f"""
            <table class="nc-table">
              <thead><tr><th>Move</th><th>Avoided exits</th><th>Gross value</th><th>Cost</th><th>Expected net</th><th>Break-even</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Marginal figures are expected values under the selected efficacy. They are scenario outputs, not observed pilot results.")

        st.markdown("### How the expected financial bridge works")
        baseline = result.baseline_expected_cost_m
        after_saving = baseline - result.gross_avoided_m
        bridge = pd.DataFrame(
            [
                {"step": "Status quo", "start": 0.0, "end": baseline, "label": money(baseline), "type": "Total"},
                {"step": "Exposure avoided", "start": after_saving, "end": baseline, "label": f"−{money(result.gross_avoided_m)}", "type": "Benefit"},
                {"step": "Programme spend", "start": after_saving, "end": result.expected_after_cost_m, "label": f"+{money(result.programme_cost_m)}", "type": "Spend"},
                {"step": "Expected after", "start": 0.0, "end": result.expected_after_cost_m, "label": money(result.expected_after_cost_m), "type": "Total"},
            ]
        )
        chart = (
            alt.Chart(bridge)
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=55)
            .encode(
                x=alt.X("step:N", title=None, sort=bridge["step"].tolist(), axis=alt.Axis(labelAngle=0)),
                y=alt.Y("start:Q", title="Expected annual people cost (A$M)", scale=alt.Scale(domain=[0, max(baseline, result.expected_after_cost_m) * 1.15])),
                y2="end:Q",
                color=alt.Color("type:N", legend=None, scale=alt.Scale(domain=["Total", "Benefit", "Spend"], range=[PURPLE, MINT, MAGENTA])),
                tooltip=["step:N", alt.Tooltip("start:Q", format=".2f"), alt.Tooltip("end:Q", format=".2f")],
            )
        )
        labels = alt.Chart(bridge).mark_text(dy=-10, color=TEXT, fontSize=13, fontWeight=600).encode(
            x=alt.X("step:N", sort=bridge["step"].tolist()), y="end:Q", text="label:N"
        )
        st.altair_chart(altair_theme((chart + labels).properties(height=300)), width="stretch")

        st.markdown("### Compare every C/D/E combination")
        combo = combination_results(efficacy, pulse, costs["C"], costs["D"], costs["E"])
        combo["selected"] = combo["strategy"].eq(key)
        combo_chart = (
            alt.Chart(combo)
            .mark_rule(strokeWidth=4, strokeCap="round")
            .encode(
                y=alt.Y("strategy:N", title=None, sort=alt.EncodingSortField(field="median", order="ascending")),
                x=alt.X("p05:Q", title="Total cost including programme spend (A$M, median and 90% range)", scale=alt.Scale(zero=False)),
                x2="p95:Q",
                color=alt.condition("datum.selected", alt.value(MINT), alt.value(GRID)),
                tooltip=["strategy:N", alt.Tooltip("p05:Q", format=".2f"), alt.Tooltip("median:Q", format=".2f"), alt.Tooltip("p95:Q", format=".2f"), alt.Tooltip("expected_net:Q", format=".2f", title="Expected net A$M")],
            )
        )
        dots = alt.Chart(combo).mark_point(filled=True, size=95).encode(
            y=alt.Y("strategy:N", sort=alt.EncodingSortField(field="median", order="ascending")),
            x="median:Q",
            color=alt.condition("datum.selected", alt.value(MINT), alt.value(PURPLE)),
        )
        status_line = alt.Chart(pd.DataFrame({"x": [scenario["reference"]["NONE"]["median_m"]]})).mark_rule(color=AMBER, strokeDash=[4, 4]).encode(x="x:Q")
        st.altair_chart(altair_theme((combo_chart + dots + status_line).properties(height=330)), width="stretch")
        st.caption("The selected combination is highlighted. Pairwise combinations are derived from the finalized segment baselines and the current assumptions; they were not printed as standalone outputs in the notebook.")

    st.markdown("## Hiring efficiency · a separate cost lever")
    hiring = data["hiring"]
    st.markdown('<span class="nc-badge nc-badge-assumption">Not included in retention scenario</span>', unsafe_allow_html=True)
    left, right = st.columns([1, 1.2])
    with left:
        shift = st.slider("Agency volume shifted to direct", 0, 75, 50, 5, format="%d%%")
        savings = hiring["agency_hires_pa"] * shift / 100 * hiring["premium_per_hire"] / 1e6
        hires_shifted = hiring["agency_hires_pa"] * shift / 100
        kpi_grid(
            [
                ("Agency hires / year", f"{hiring['agency_hires_pa']:.0f}", "CY2024–25 average"),
                ("Hires moved to direct", f"{hires_shifted:.0f}", f"{shift}% scenario"),
                ("Gross premium addressed", money(savings, 2), "before internal sourcing and vacancy costs"),
            ]
        )
    with right:
        st.markdown(
            f"""
            <div class="nc-card">
              <span class="nc-badge nc-badge-evidence">Matched comparison</span>
              <div class="nc-card-title">A {hiring['fee_ratio']:.1f}× fee buys no obvious quality advantage</div>
              <div class="nc-card-copy">Average Agency fee {money(hiring['average_agency_fee']/1e6,3)} per hire versus A${hiring['direct_benchmark']:,.0f} Direct benchmark. In {hiring['matched_strata']} role-family × level × year strata, early-exit rates were {hiring['agency_matched_early_pct']:.2f}% Agency versus {hiring['direct_matched_early_pct']:.2f}% Direct.</div>
              <div class="nc-card-action"><b>Boundary:</b> treat the result as gross addressable premium until recruiter capacity, fill rate, vacancy duration, quality and diversity are measured.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def evidence_card(title: str, evidence: str, decision: str, boundary: str, badge: str = "Validated evidence") -> str:
    badge_class = "nc-badge-evidence" if badge == "Validated evidence" else "nc-badge-assumption"
    return f"""
    <div class="nc-evidence">
      <span class="nc-badge {badge_class}">{badge}</span>
      <h4>{title}</h4>
      <dl>
        <dt>Evidence</dt><dd>{evidence}</dd>
        <dt>Supported decision</dt><dd>{decision}</dd>
        <dt>Boundary</dt><dd>{boundary}</dd>
      </dl>
    </div>
    """


def evidence_page(data: dict) -> None:
    finance = data["finance"]
    measurement = data["measurement"]
    warning = data["warning"]
    drivers = data["drivers"]
    scenario = data["scenario"]
    interventions = {row["code"]: row for row in data["interventions"]}

    page_title(
        "Evidence, assumptions and controls",
        "Every recommendation has an evidence boundary.",
        "This is the audit trail behind the dashboard: what was observed, what is assumed for planning, what should be measured next, and what NovaCorp must never do with employee data.",
    )
    tabs = st.tabs(["Evidence map", "Assumptions", "Pilot scorecard", "Governance"])

    with tabs[0]:
        st.markdown("### Observation → decision")
        cards = [
            (
                "The real target costs A$27.5M/year",
                f"{finance['genuine_exits_2y']} voluntary + pull + high-value exits over 24 months; {finance['replacement_formula']}.",
                "Treat genuine regrettable attrition as the principal retention problem.",
                "Replacement exposure is a decision ceiling, not guaranteed savings.",
            ),
            (
                "The existing HR flag sees barely a third",
                f"Recall {measurement['recall_pct']:.1f}%; {measurement['fn']} exits and {money(measurement['missed_m'])}/year missed.",
                "Replace the flag with the finalized three-field measurement rule.",
                "The new rule is a definition and review process—not an employee flight-risk model.",
            ),
            (
                "Engagement provides no usable target warning",
                f"Last response {warning['headline_last_z']:.2f}z vs stayers {warning['stayer_last_z']:.2f}z (p={warning['p_value']:.2f}); {warning['headline_pct']:.0f}% still responded.",
                "Use structural retention programmes; keep survey outreach confidential and voluntary.",
                "The analysis covers respondents and does not prove every behavioural signal is absent.",
            ),
            (
                "HiPos are a higher-rate cohort",
                f"{drivers['hipo']['rate']:.2f} vs {drivers['hipo']['other_rate']:.2f} exits per 100 person-years; RR {drivers['hipo']['rr']:.2f}, 95% CI {drivers['hipo']['low']:.2f}–{drivers['hipo']['high']:.2f}.",
                "Pilot C: progression criteria, career conversations and a small promotion pool.",
                "Association is strong but programme efficacy remains untested.",
            ),
            (
                "Integration risk arrives on a calendar",
                f"Entity C corrected first-year rate {drivers['integration']['entity_c_first_year_rate']:.2f} vs Origin {drivers['integration']['origin_first_year_rate']:.2f}; finalized 2026 pulse {drivers['integration']['pulse_2026']:.1f} exits.",
                "Pilot D before the known consolidation milestone.",
                "Entity B's corrected first-year rate is below Origin; the case rests on event timing, not a uniformly higher rate.",
            ),
            (
                "R&C pressure is triangulated, but small-sample",
                f"L4+ rate {drivers['rc']['senior_rate']:.1f}/100 person-years from {drivers['rc']['senior_exits']} exits; {drivers['rc']['waves']} below-firm confidence waves.",
                "Pilot E: FAR readiness, role clarity and accountability support.",
                "The senior exit result rests on five exits; do not rank teams or managers.",
            ),
        ]
        for start in range(0, len(cards), 2):
            columns = st.columns(2)
            for column, card in zip(columns, cards[start : start + 2]):
                with column:
                    st.markdown(evidence_card(*card), unsafe_allow_html=True)

        st.markdown("### Where the other factors went")
        decision_rows = "".join(
            f"<tr><td><b>{item['decision']}</b></td><td>{item['reason']}</td></tr>"
            for item in data["decisions_not_modelled"]
        )
        st.markdown(
            f'<table class="nc-table"><thead><tr><th>Decision</th><th>Why it is not a C/D/E scenario lever</th></tr></thead><tbody>{decision_rows}</tbody></table>',
            unsafe_allow_html=True,
        )

    with tabs[1]:
        st.markdown("### Three layers keep evidence separate from judgment")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(
                f"""
                <div class="nc-card"><span class="nc-badge nc-badge-evidence">Locked evidence</span><div class="nc-card-title">Observed and reconciled</div><div class="nc-card-copy">{finance['genuine_exits_2y']} exits; {money(finance['regrettable_m'])}/year; HiPo RR {drivers['hipo']['rr']:.2f}; current-flag recall {measurement['recall_pct']:.1f}%.</div><div class="nc-card-action">These values do not change in the simulator.</div></div>
                """,
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f"""
                <div class="nc-card"><span class="nc-badge nc-badge-assumption">Notebook assumptions</span><div class="nc-card-title">Finalized planning baseline</div><div class="nc-card-copy">{scenario['expected_exits']:.0f} expected 2026 exits; {money(scenario['expected_cost_m'])}; Beta(3.5, 8) efficacy prior; {scenario['entity_pulse_exits']:.1f}-exit integration pulse.</div><div class="nc-card-action">Locked reference outputs use {scenario['simulations']:,} simulations.</div></div>
                """,
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                """
                <div class="nc-card"><span class="nc-badge nc-badge-scenario">Explore mode</span><div class="nc-card-title">User-defined scenario</div><div class="nc-card-copy">Programme combination, efficacy, pulse size and programme costs can be changed for planning.</div><div class="nc-card-action">Every changed result is labelled derived scenario output.</div></div>
                """,
                unsafe_allow_html=True,
            )

        assumption_rows = f"""
        <tr><td>Replacement exposure</td><td>Salary × 1.5 × 85% backfill</td><td>Finance constant</td><td>Cost per exit</td></tr>
        <tr><td>Efficacy</td><td>Beta(3.5, 8), mean {scenario['efficacy_mean_pct']:.1f}%</td><td>Planning prior</td><td>Share of reachable exits prevented</td></tr>
        <tr><td>Integration pulse</td><td>{scenario['entity_pulse_exits']:.1f} incremental exits</td><td>Event scenario</td><td>D's reachable exposure</td></tr>
        <tr><td>Programme costs</td><td>C {money(interventions['C']['cost_m'])}; D {money(interventions['D']['cost_m'])}; E {money(interventions['E']['cost_m'])}</td><td>Notebook design</td><td>Total cost after action</td></tr>
        """
        st.markdown(
            f'<table class="nc-table"><thead><tr><th>Assumption</th><th>Finalized default</th><th>Source type</th><th>What it changes</th></tr></thead><tbody>{assumption_rows}</tbody></table>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="nc-warning"><b>Disengagement boundary:</b> {money(finance["disengagement_finance_m"])} reproduces Finance’s 15% loss assumption, but the observed goal-score gap supports only {money(finance["disengagement_observed_m"],2)} and is statistically inconclusive (p={finance["disengagement_p"]:.2f}).</div>',
            unsafe_allow_html=True,
        )

    with tabs[2]:
        st.markdown("### What must be observed before scaling")
        scorecards = [
            ("C · Career progression", "Delivery", "Career conversations, documented criteria and 20 accelerated promotions", "365-day high-value pull-exit rate; internal mobility and promotion", "Stop for no credible improvement or unfair access"),
            ("D · Integration playbook", "Event window", "Milestone communications, role clarity and retention conversations", "Consolidation-linked excess exits versus the predeclared 16-exit pulse", "Stop if the pulse is not materially reduced"),
            ("E · FAR readiness", "12 months", "Readiness completion, accountability support and role clarity", "L4+ exit rate and confidence-in-role-future trend", "Stop for no credible improvement"),
            ("Portfolio", "12 months", "Programme spend and delivery fidelity", "Avoided replacement exposure and realized net value against comparison group", "Do not scale without positive net value"),
            ("Fairness", "Every review", "Access and participation by sufficiently large subgroup", "Selection, participation and outcome gaps", "Fairness is a stopping condition"),
            ("Measurement", "Quarterly", "Three-field rule coverage and exit-record reconciliation", "Review volume, outcome quality and historical comparability", "No employee risk scores or manager league tables"),
        ]
        for start in range(0, len(scorecards), 3):
            columns = st.columns(3)
            for column, item in zip(columns, scorecards[start : start + 3]):
                with column:
                    title, timing, delivery, outcome, stop = item
                    st.markdown(
                        f"""
                        <div class="nc-evidence"><span class="nc-badge nc-badge-scenario">Future observed</span><h4>{title}</h4><dl><dt>Measured at</dt><dd>{timing}</dd><dt>Delivery</dt><dd>{delivery}</dd><dt>Outcome</dt><dd>{outcome}</dd><dt>Stop if</dt><dd>{stop}</dd></dl></div>
                        """,
                        unsafe_allow_html=True,
                    )

    with tabs[3]:
        left, right = st.columns(2)
        with left:
            st.markdown("### Use the dashboard for")
            st.markdown(
                """
                <div class="nc-summary">
                ✓ Portfolio planning and break-even discussion<br><br>
                ✓ Selecting bounded pilot interventions<br><br>
                ✓ Comparing do-nothing and action scenarios<br><br>
                ✓ Pre-registering outcomes and stopping conditions<br><br>
                ✓ Reviewing aggregate, sufficiently large cohorts
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown("### Never use the dashboard for")
            st.markdown(
                """
                <div class="nc-danger">
                ✕ Employee flight-risk rankings or “likely leaver” labels<br><br>
                ✕ Promotion, discipline or manager performance decisions<br><br>
                ✕ Publishing manager league tables or cells below ten<br><br>
                ✕ Treating exposure as guaranteed savings<br><br>
                ✕ Claiming scenario output proves causal programme efficacy
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("### Technical provenance")
        st.markdown(
            """
            <div class="nc-card"><div class="nc-card-title">Finalized and public-safe</div><div class="nc-card-copy">Evidence window CY2024–CY2025 · finalized NovaCorp Story · Finance constants 1.5× replacement and 85% backfill · aggregate snapshot only.</div><div class="nc-card-action">The public project contains no employee names, employee IDs, manager IDs, reviewer IDs or original row-level HR tables.</div></div>
            """,
            unsafe_allow_html=True,
        )


inject_css()
snapshot = load_snapshot()

with st.sidebar:
    st.markdown("## NovaCorp")
    st.caption("Decision Lab · Final story standard")
    page = st.radio(
        "Navigation",
        ["Decision overview", "Strategy simulator", "Evidence & controls"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown('<span class="nc-badge nc-badge-evidence">Aggregate only</span>', unsafe_allow_html=True)
    st.caption("CY2024–CY2025 evidence · A$ · annualised where stated")
    st.caption("Scenario outputs are conditional planning estimates, not employee predictions.")

if page == "Decision overview":
    overview_page(snapshot)
elif page == "Strategy simulator":
    scenario_page(snapshot)
else:
    evidence_page(snapshot)

st.divider()
st.caption("NovaCorp Decision Lab · finalized evidence snapshot · public-safe aggregate design")
