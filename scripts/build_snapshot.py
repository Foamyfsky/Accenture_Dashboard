#!/usr/bin/env python3
"""Build the single aggregate snapshot used by the public dashboard.

Inputs are the finalized NovaCorp_Story notebook and the four original source
tables. The generated JSON contains aggregate facts only: no employee, manager,
reviewer, or name fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


W0 = pd.Timestamp("2024-01-01")
W1 = pd.Timestamp("2025-12-31")
YEARS = 2.0
MULT = 1.5
BACKFILL = 0.85
SUPER = 0.12
AGENCY_FEE = 0.18
DIRECT_COST = 5_500
HIGH_BANDS = ["Outstanding", "High Performer"]
ENG_DIMS = [
    "manager_effectiveness",
    "psychological_safety",
    "recognition",
    "career_development",
    "senior_leadership_trust",
    "purpose_meaning",
    "wellbeing",
    "confidence_in_role_future",
]
SEGS = ["HiPo", "Entity_B/C", "R&C", "base"]
AUTHORITATIVE_NOTEBOOK_SHA256 = "4d6372ec6e4b93e8c6c9da9e723b65f421ab9f4d34470366e4dc28b0b7cc3068"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def annual_cost_m(frame: pd.DataFrame, salary_col: str = "salary_at_exit") -> float:
    return float((frame[salary_col] * MULT * BACKFILL).sum() / 1e6 / YEARS)


def person_years(frame: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp) -> pd.Series:
    begins = frame["hire_date"].clip(lower=start)
    ends = frame["exit_date"].fillna(end).clip(upper=end)
    return ((ends - begins).dt.days.clip(lower=0)) / 365.25


def round_tree(value):
    if isinstance(value, dict):
        return {key: round_tree(item) for key, item in value.items()}
    if isinstance(value, list):
        return [round_tree(item) for item in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        if math.isnan(float(value)):
            return None
        return round(float(value), 6)
    return value


def build(raw_dir: Path, notebook: Path, output: Path) -> None:
    notebook_sha = digest(notebook)
    if notebook_sha != AUTHORITATIVE_NOTEBOOK_SHA256:
        raise ValueError(
            "The notebook does not match the finalized NovaCorp_Story version. "
            f"Expected {AUTHORITATIVE_NOTEBOOK_SHA256}, received {notebook_sha}."
        )

    employees = pd.read_csv(raw_dir / "employees.csv", parse_dates=["hire_date", "exit_date"])
    attrition = pd.read_csv(raw_dir / "attrition_log.csv", parse_dates=["exit_date"])
    performance = pd.read_csv(raw_dir / "performance.csv", parse_dates=["review_date"])
    engagement = pd.read_csv(raw_dir / "engagement.csv", parse_dates=["survey_date"])

    exits = attrition.merge(employees.drop(columns=["exit_date"]), on="employee_id", validate="1:1")
    exits["high_value"] = exits["performance_band_at_exit"].isin(HIGH_BANDS) | exits["hipo_flag"]
    exits["headline"] = (
        exits["exit_type"].eq("voluntary")
        & exits["pathway"].eq("pull")
        & exits["high_value"]
    )
    headline = exits[exits["headline"]].copy()
    headline_ids = set(headline["employee_id"])

    # Measurement and Finance reconciliation.
    tp = int((exits["headline"] & exits["regrettable_flag"]).sum())
    fn = int((exits["headline"] & ~exits["regrettable_flag"]).sum())
    fp = int((~exits["headline"] & exits["regrettable_flag"]).sum())
    seen = exits[exits["headline"] & exits["regrettable_flag"]]
    missed = exits[exits["headline"] & ~exits["regrettable_flag"]]

    engagement["composite"] = engagement[ENG_DIMS].mean(axis=1)
    responded = engagement[engagement["response_flag"]]
    eng_emp = (
        responded.groupby("employee_id")
        .agg(responses=("wave_number", "size"), mean_engagement=("composite", "mean"))
        .join(employees.set_index("employee_id")[["salary"]])
    )
    eng_emp = eng_emp[eng_emp["responses"] >= 3]
    persistent = eng_emp[eng_emp["mean_engagement"] <= 2.5]
    finance_disengagement_m = float((persistent["salary"] * 0.15).sum() / 1e6)
    goal_mean = performance.groupby("employee_id")["goal_achievement_score"].mean()
    eng_goals = eng_emp.join(goal_mean.rename("goal"))
    low = eng_goals[eng_goals["mean_engagement"] <= 2.5]["goal"].dropna()
    other = eng_goals[eng_goals["mean_engagement"] > 2.5]["goal"].dropna()
    goal_gap_points = float(other.mean() - low.mean())
    goal_gap_relative = float(goal_gap_points / other.mean())
    observed_disengagement_m = float(len(persistent) * persistent["salary"].mean() * goal_gap_relative / 1e6)
    disengagement_p = float(stats.mannwhitneyu(other, low)[1])

    hires = employees.copy()
    hires["hire_year"] = hires["hire_date"].dt.year
    hires["early_12"] = hires["status"].eq("departed") & hires["tenure_months"].lt(12)
    agency = hires[hires["hire_source"].eq("agency")].copy()
    agency["fee"] = agency["salary"] * AGENCY_FEE
    agency["premium"] = agency["fee"] - DIRECT_COST
    agency_window = agency[agency["hire_date"].between(W0, W1)]
    agency_premium_pa = float(agency_window["premium"].sum() / 1e6 / YEARS)
    recruited = hires[hires["hire_source"].isin(["agency", "direct", "referral", "graduate"])]
    early = recruited[recruited["early_12"]]
    early_cost_pa = annual_cost_m(early, "salary")
    hiring_bucket_pa = agency_premium_pa + early_cost_pa

    origin = recruited[recruited["legacy_entity_code"].eq("NovaCorp-Origin")].copy()
    origin["early_24"] = origin["status"].eq("departed") & origin["tenure_months"].lt(24)
    ad = origin[origin["hire_source"].isin(["agency", "direct"])]
    match_keys = ["role_family", "role_level", "hire_year"]
    channel_counts = ad.groupby(match_keys + ["hire_source"]).size().unstack(fill_value=0)
    both = channel_counts[(channel_counts.get("agency", 0) > 0) & (channel_counts.get("direct", 0) > 0)].index
    matched = ad.set_index(match_keys).loc[both].reset_index()
    matched_channel = matched.groupby("hire_source").agg(
        hires=("employee_id", "size"),
        days=("days_to_fill", "mean"),
        early=("early_12", "mean"),
        hipo=("hipo_flag", "mean"),
    )

    bucket1 = annual_cost_m(headline)
    bucket2 = finance_disengagement_m
    bucket3 = hiring_bucket_pa

    # Engagement warning evidence.
    resp = engagement[engagement["response_flag"]].copy()
    resp["z"] = resp.groupby("wave_number")["composite"].transform(lambda x: (x - x.mean()) / x.std())
    first_response = resp.sort_values("wave_number").groupby("employee_id")["composite"].first()
    resp["own_change"] = resp["composite"] - resp["employee_id"].map(first_response)
    push_ids = set(exits[(exits["exit_type"].eq("voluntary")) & exits["pathway"].eq("push")]["employee_id"])

    def warning_group(eid: str) -> str:
        if eid in headline_ids:
            return "headline"
        if eid in push_ids:
            return "push"
        return "other"

    with_exit = resp.merge(attrition[["employee_id", "exit_date"]], on="employee_id", how="left")
    pre_exit = with_exit[with_exit["exit_date"].notna() & (with_exit["survey_date"] < with_exit["exit_date"])]
    last_completed = pre_exit.sort_values("survey_date").groupby("employee_id").tail(1).copy()
    last_completed["group"] = last_completed["employee_id"].map(warning_group)
    stayers = with_exit[with_exit["exit_date"].isna()].sort_values("survey_date").groupby("employee_id").tail(1).copy()
    stayers["group"] = "stayers"
    final_response = pd.concat([last_completed, stayers])
    headline_last = final_response[final_response["group"].eq("headline")]
    stayer_last = final_response[final_response["group"].eq("stayers")]
    warning_p = float(stats.ttest_ind(headline_last["z"], stayer_last["z"], equal_var=False).pvalue)

    all_issued = engagement.merge(attrition[["employee_id", "exit_date"]], on="employee_id", how="left")
    issued_pre_exit = all_issued[all_issued["exit_date"].notna() & (all_issued["survey_date"] < all_issued["exit_date"])]
    last_issued = issued_pre_exit.sort_values("survey_date").groupby("employee_id").tail(1).copy()
    last_issued["group"] = last_issued["employee_id"].map(warning_group)
    stayer_wave5 = engagement[(engagement["wave_number"].eq(5)) & ~engagement["employee_id"].isin(attrition["employee_id"])]
    response_rates = {
        "headline_pct": 100 * last_issued[last_issued["group"].eq("headline")]["response_flag"].mean(),
        "push_pct": 100 * last_issued[last_issued["group"].eq("push")]["response_flag"].mean(),
        "stayers_pct": 100 * stayer_wave5["response_flag"].mean(),
    }

    # Driver evidence.
    emp_rate = employees.copy()
    emp_rate["py"] = ((emp_rate["exit_date"].fillna(W1) - emp_rate["hire_date"].clip(lower=W0)).dt.days / 365.25).clip(lower=1 / 365.25)
    perf_pull = exits[
        exits["exit_type"].eq("voluntary")
        & exits["pathway"].eq("pull")
        & exits["performance_band_at_exit"].isin(HIGH_BANDS)
    ]
    emp_rate["perf_pull"] = emp_rate["employee_id"].isin(perf_pull["employee_id"]).astype(int)
    rates = emp_rate.groupby("hipo_flag").agg(n=("employee_id", "size"), py=("py", "sum"), exits=("perf_pull", "sum"))
    rates["rate"] = rates["exits"] / rates["py"] * 100
    rr = float(rates.loc[True, "rate"] / rates.loc[False, "rate"])
    se = math.sqrt(1 / rates.loc[True, "exits"] + 1 / rates.loc[False, "exits"])
    rr_low = math.exp(math.log(rr) - 1.96 * se)
    rr_high = math.exp(math.log(rr) + 1.96 * se)

    driver_frame = headline.copy()
    driver_frame["hipo_driver"] = driver_frame["hipo_flag"]
    driver_frame["entity_driver"] = driver_frame["legacy_entity_code"].isin(["Entity_B", "Entity_C"])
    driver_frame["rc_driver"] = driver_frame["department"].eq("Risk & Compliance")
    driver_union = driver_frame[driver_frame[["hipo_driver", "entity_driver", "rc_driver"]].any(axis=1)]
    residual = driver_frame[~driver_frame[["hipo_driver", "entity_driver", "rc_driver"]].any(axis=1)]

    new_hires = employees[employees["hire_date"] >= W0].copy()
    horizon = new_hires["hire_date"] + pd.Timedelta(days=365)
    new_hires["exp"] = (
        new_hires["exit_date"].fillna(W1).clip(upper=horizon) - new_hires["hire_date"]
    ).dt.days.clip(lower=1) / 365.25
    new_hires["event"] = (new_hires["employee_id"].isin(headline_ids) & (new_hires["exit_date"] <= horizon)).astype(int)
    fair = new_hires.groupby("legacy_entity_code").agg(n=("employee_id", "size"), py=("exp", "sum"), exits=("event", "sum"))
    fair["rate"] = fair["exits"] / fair["py"] * 100

    emp_rate["headline"] = emp_rate["employee_id"].isin(headline_ids).astype(int)
    senior = emp_rate[emp_rate["role_level"] >= 4]
    senior_rates = senior.groupby("department").agg(py=("py", "sum"), exits=("headline", "sum"))
    senior_rates["rate"] = senior_rates["exits"] / senior_rates["py"] * 100
    rc_senior = senior_rates.loc["Risk & Compliance"]
    rc_conf = engagement[engagement["response_flag"]].copy()
    rc_conf["z"] = rc_conf.groupby("wave_number")["confidence_in_role_future"].transform(lambda x: (x - x.mean()) / x.std())
    rc_conf = rc_conf.merge(employees[["employee_id", "department", "role_level"]], on="employee_id")
    rc_conf = rc_conf[(rc_conf["department"].eq("Risk & Compliance")) & (rc_conf["role_level"] >= 3)]
    rc_wave = rc_conf.groupby("wave_number")["z"].mean()

    # Scenario segmentation and baseline exactly reproduce the notebook.
    sim_emp = employees.copy()
    sim_emp["segment"] = "base"
    sim_emp.loc[sim_emp["department"].eq("Risk & Compliance"), "segment"] = "R&C"
    sim_emp.loc[sim_emp["legacy_entity_code"].isin(["Entity_B", "Entity_C"]), "segment"] = "Entity_B/C"
    sim_emp.loc[sim_emp["hipo_flag"], "segment"] = "HiPo"
    sim_emp["py24"] = person_years(sim_emp, pd.Timestamp("2024-01-01"), pd.Timestamp("2024-12-31"))
    sim_emp["py25"] = person_years(sim_emp, pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31"))
    exit_date_lookup = headline.set_index("employee_id")["exit_date"]
    sim_emp["x24"] = sim_emp["employee_id"].map(
        lambda eid: int(eid in headline_ids and pd.Timestamp("2024-01-01") <= exit_date_lookup[eid] <= pd.Timestamp("2024-12-31"))
    )
    sim_emp["x25"] = sim_emp["employee_id"].map(
        lambda eid: int(eid in headline_ids and pd.Timestamp("2025-01-01") <= exit_date_lookup[eid] <= pd.Timestamp("2025-12-31"))
    )
    active = sim_emp[sim_emp["status"].eq("active")]
    heads = active.groupby("segment").size().reindex(SEGS)
    py2 = (sim_emp.groupby("segment")["py24"].sum() + sim_emp.groupby("segment")["py25"].sum()).reindex(SEGS)
    x2 = (sim_emp.groupby("segment")["x24"].sum() + sim_emp.groupby("segment")["x25"].sum()).reindex(SEGS)
    blended = x2 / py2
    severity = (
        headline.merge(sim_emp[["employee_id", "segment"]], on="employee_id")
        .groupby("segment")["salary_at_exit"].mean()
        * MULT
        * BACKFILL
        / 1e6
    ).reindex(SEGS)

    entity_segment_exits = headline.merge(sim_emp[["employee_id", "segment"]], on="employee_id")
    entity_segment_exits = entity_segment_exits[entity_segment_exits["segment"].eq("Entity_B/C")]
    entity_baseline = 2 * len(entity_segment_exits[entity_segment_exits["exit_date"] >= pd.Timestamp("2025-07-01")])
    entity_b_active = int((active["legacy_entity_code"].eq("Entity_B")).sum())
    entity_b_all = int((sim_emp["legacy_entity_code"].eq("Entity_B")).sum())
    pulse = 19 * entity_b_active / entity_b_all
    mu = pd.Series(index=SEGS, dtype=float)
    for segment in ["HiPo", "R&C", "base"]:
        mu[segment] = blended[segment] * heads[segment]
    mu["Entity_B/C"] = entity_baseline + pulse

    # Programme costs.
    midpoint = (sim_emp["salary"] / sim_emp["compa_ratio"]).groupby(sim_emp["role_level"]).median()
    active_hipo = active[active["hipo_flag"]].copy()
    cost_a = float(np.maximum(0, 0.95 * active_hipo["salary"] / active_hipo["compa_ratio"] - active_hipo["salary"]).sum() * (1 + SUPER) / 1e6)
    eligible = active_hipo[active_hipo["promotion_eligible"]].copy()
    eligible["step"] = np.maximum(
        eligible["role_level"].add(1).map(midpoint) * 0.90 - eligible["salary"],
        0.05 * eligible["salary"],
    )
    cost_b = float(eligible["step"].sum() * (1 + SUPER) / 1e6)
    cost_c = float(len(active_hipo) * 800 / 1e6 + 20 * eligible["step"].mean() * (1 + SUPER) / 1e6)
    cost_d, cost_e = 1.0, 0.6
    eligible_coverage = float(headline[headline["hipo_flag"]]["promotion_eligible"].mean())

    addressable = {
        "A": float(mu["HiPo"] * severity["HiPo"]),
        "B": float(mu["HiPo"] * severity["HiPo"]),
        "C": float(mu["HiPo"] * severity["HiPo"]),
        "D": float(pulse * severity["Entity_B/C"]),
        "E": float(mu["R&C"] * severity["R&C"]),
    }
    costs = {"A": cost_a, "B": cost_b, "C": cost_c, "D": cost_d, "E": cost_e}
    coverage = {"A": 1.0, "B": eligible_coverage, "C": 1.0, "D": 1.0, "E": 1.0}

    # Exact notebook reference simulation sequence.
    rng = np.random.default_rng(42)
    n = 10_000

    def simulate_base() -> np.ndarray:
        return sum(rng.poisson(mu[s], n) * severity[s] for s in SEGS)

    def simulate_single(cost: float, target: str | None, pulse_target: bool = False) -> np.ndarray:
        efficacy = rng.beta(3.5, 8, n)
        arrays = {s: np.full(n, mu[s]) for s in SEGS}
        if target:
            arrays[target] = mu[target] * (1 - efficacy)
        if pulse_target:
            arrays["Entity_B/C"] = entity_baseline + pulse * (1 - efficacy)
        return sum(rng.poisson(np.broadcast_to(arrays[s], n)) * severity[s] for s in SEGS) + cost

    base_draw = simulate_base()
    reference_draws = {
        "NONE": base_draw,
        "C": simulate_single(cost_c, "HiPo"),
        "D": simulate_single(cost_d, None, pulse_target=True),
        "E": simulate_single(cost_e, "R&C"),
    }
    eff_c, eff_d, eff_e = rng.beta(3.5, 8, (3, n))
    portfolio = rng.poisson(mu["HiPo"] * (1 - eff_c), n) * severity["HiPo"]
    portfolio += rng.poisson(entity_baseline + pulse * (1 - eff_d), n) * severity["Entity_B/C"]
    portfolio += rng.poisson(mu["R&C"] * (1 - eff_e), n) * severity["R&C"]
    portfolio += rng.poisson(mu["base"], n) * severity["base"]
    portfolio += cost_c + cost_d + cost_e
    reference_draws["C+D+E"] = portfolio
    reference = {}
    for key, draw in reference_draws.items():
        p05, median, p95 = np.percentile(draw, [5, 50, 95])
        reference[key] = {
            "p05_m": p05,
            "median_m": median,
            "p95_m": p95,
            "difference_m": median - np.median(base_draw),
            "probability_lower_pct": None if key == "NONE" else 100 * (draw < base_draw).mean(),
        }

    # Back-test summary.
    backtest = sim_emp.groupby("segment").agg(py24=("py24", "sum"), x24=("x24", "sum"), py25=("py25", "sum"), x25=("x25", "sum")).reindex(SEGS)
    backtest["predicted25"] = backtest["x24"] / backtest["py24"] * backtest["py25"]

    interventions = [
        {
            "code": "A",
            "name": "Blanket HiPo pay fix",
            "status": "Rejected",
            "problem": "HiPos sit at 0.88 compa-ratio versus 0.95 for others, but pay is not a proven causal trigger.",
            "action": "Raise all active HiPos to 0.95 compa-ratio.",
            "owner": "Talent & Reward",
            "cost_m": costs["A"],
            "addressable_m": addressable["A"],
            "coverage_pct": 100,
            "break_even_pct": costs["A"] / addressable["A"] * 100,
            "boundary": "Annual cost exceeds the entire HiPo exposure; impossible to break even.",
        },
        {
            "code": "B",
            "name": "Blanket promotion",
            "status": "Rejected",
            "problem": "Progression congestion is plausible, but eligible employees carried only about 27% of HiPo exit exposure.",
            "action": "Promote every promotion-eligible active HiPo.",
            "owner": "Talent & Reward",
            "cost_m": costs["B"],
            "addressable_m": addressable["B"],
            "coverage_pct": coverage["B"] * 100,
            "break_even_pct": costs["B"] / (addressable["B"] * coverage["B"]) * 100,
            "boundary": "Most spending falls outside the reachable exposure; impossible to break even.",
        },
        {
            "code": "C",
            "name": "HiPo career programme",
            "short_name": "Career progression",
            "status": "Pilot",
            "target_segment": "HiPo",
            "problem": "Recognition as a future leader is not matched by pay positioning and visible progression.",
            "evidence": f"HiPo exit RR {rr:.2f} (95% CI {rr_low:.2f}–{rr_high:.2f}); A${annual_cost_m(driver_frame[driver_frame['hipo_driver']]):.1f}M historical exposure.",
            "action": "Progression criteria, structured career conversations and 20 accelerated promotions per year.",
            "owner": "Talent & Reward",
            "cost_m": costs["C"],
            "addressable_m": addressable["C"],
            "reachable_exits": mu["HiPo"],
            "break_even_pct": costs["C"] / addressable["C"] * 100,
            "boundary": "The association is strong; programme efficacy is not yet causal evidence.",
        },
        {
            "code": "D",
            "name": "Entity B milestone playbook",
            "short_name": "Integration playbook",
            "status": "Pilot",
            "target_segment": "Entity_B/C",
            "problem": "Integration-linked exits arrive around known milestones rather than as stable background churn.",
            "evidence": f"Finalized 2026 pulse assumption: {pulse:.1f} incremental exits, A${addressable['D']:.1f}M exposure.",
            "action": "Role clarity, communications and retention conversations before the consolidation milestone.",
            "owner": "Integration Programme",
            "cost_m": costs["D"],
            "addressable_m": addressable["D"],
            "reachable_exits": pulse,
            "break_even_pct": costs["D"] / addressable["D"] * 100,
            "boundary": "A time-sensitive planning scenario; it is below break-even at 30% efficacy on a standalone basis.",
        },
        {
            "code": "E",
            "name": "R&C FAR readiness",
            "short_name": "FAR readiness",
            "status": "Pilot",
            "target_segment": "R&C",
            "problem": "Senior R&C roles combine elevated exits with persistent uncertainty about role futures.",
            "evidence": f"L4+ rate {rc_senior['rate']:.1f}/100 person-years from {int(rc_senior['exits'])} exits; five below-firm survey waves.",
            "action": "FAR readiness, accountability support, role clarity and market benchmarking.",
            "owner": "CRO with HR",
            "cost_m": costs["E"],
            "addressable_m": addressable["E"],
            "reachable_exits": mu["R&C"],
            "break_even_pct": costs["E"] / addressable["E"] * 100,
            "boundary": "Senior-rate evidence rests on five exits; triangulation, not sample size, supports the pilot.",
        },
    ]

    snapshot = {
        "metadata": {
            "title": "NovaCorp Decision Lab",
            "version": "final-story-1",
            "window": "CY2024–CY2025",
            "currency": "A$",
            "notebook_sha256": notebook_sha,
            "source": "NovaCorp_Story.ipynb and four original source tables",
            "public_data": "Aggregate only",
        },
        "finance": {
            "reported_total_m": 42.0,
            "rebuilt_total_m": bucket1 + bucket2 + bucket3,
            "regrettable_m": bucket1,
            "disengagement_finance_m": bucket2,
            "disengagement_observed_m": observed_disengagement_m,
            "hiring_m": bucket3,
            "genuine_exits_2y": len(headline),
            "definition": "Voluntary + employee-initiated pull + Outstanding / High Performer / HiPo",
            "replacement_formula": "Salary at exit × 1.5 × 85% backfill, annualised",
            "disengagement_gap_pct": goal_gap_relative * 100,
            "disengagement_p": disengagement_p,
        },
        "workforce": {
            "employees": len(employees),
            "active": int(employees["status"].eq("active").sum()),
            "voluntary": int(exits["exit_type"].eq("voluntary").sum()),
            "push": int((exits["exit_type"].eq("voluntary") & exits["pathway"].eq("push")).sum()),
            "pull": int((exits["exit_type"].eq("voluntary") & exits["pathway"].eq("pull")).sum()),
        },
        "measurement": {
            "tp": tp,
            "fn": fn,
            "fp": fp,
            "recall_pct": 100 * tp / (tp + fn),
            "precision_pct": 100 * tp / (tp + fp),
            "seen_m": annual_cost_m(seen),
            "missed_m": annual_cost_m(missed),
            "old_reviews_pa": (tp + fp) / YEARS,
            "new_reviews_pa": len(headline) / YEARS,
        },
        "warning": {
            "headline_last_z": float(headline_last["z"].mean()),
            "stayer_last_z": float(stayer_last["z"].mean()),
            "p_value": warning_p,
            "headline_own_change": float(headline_last["own_change"].mean()),
            "stayer_own_change": float(stayer_last["own_change"].mean()),
            "pre_exit_coverage": int(last_completed["employee_id"].isin(headline_ids).sum()),
            **response_rates,
        },
        "drivers": {
            "historical": [
                {"code": "C", "name": "HiPo career friction", "exits_2y": int(driver_frame["hipo_driver"].sum()), "cost_m": annual_cost_m(driver_frame[driver_frame["hipo_driver"]])},
                {"code": "D", "name": "Entity B/C integration", "exits_2y": int(driver_frame["entity_driver"].sum()), "cost_m": annual_cost_m(driver_frame[driver_frame["entity_driver"]])},
                {"code": "E", "name": "Risk & Compliance", "exits_2y": int(driver_frame["rc_driver"].sum()), "cost_m": annual_cost_m(driver_frame[driver_frame["rc_driver"]])},
            ],
            "union_exits_2y": len(driver_union),
            "union_cost_m": annual_cost_m(driver_union),
            "union_share_pct": 100 * annual_cost_m(driver_union) / annual_cost_m(headline),
            "residual_exits_2y": len(residual),
            "residual_cost_m": annual_cost_m(residual),
            "hipo": {
                "rate": float(rates.loc[True, "rate"]),
                "other_rate": float(rates.loc[False, "rate"]),
                "rr": rr,
                "low": rr_low,
                "high": rr_high,
                "compa": 0.88,
                "other_compa": 0.95,
            },
            "integration": {
                "entity_b_first_year_rate": float(fair.loc["Entity_B", "rate"]),
                "entity_c_first_year_rate": float(fair.loc["Entity_C", "rate"]),
                "origin_first_year_rate": float(fair.loc["NovaCorp-Origin", "rate"]),
                "pulse_2026": pulse,
                "pulse_cost_m": addressable["D"],
            },
            "rc": {
                "senior_rate": float(rc_senior["rate"]),
                "senior_exits": int(rc_senior["exits"]),
                "confidence_low": float(rc_wave.min()),
                "confidence_high": float(rc_wave.max()),
                "waves": len(rc_wave),
            },
        },
        "interventions": interventions,
        "scenario": {
            "segments": [
                {
                    "segment": s,
                    "active_headcount": int(heads[s]),
                    "expected_exits": float(mu[s]),
                    "severity_m": float(severity[s]),
                    "expected_cost_m": float(mu[s] * severity[s]),
                }
                for s in SEGS
            ],
            "entity_baseline_exits": entity_baseline,
            "entity_pulse_exits": pulse,
            "expected_exits": float(mu.sum()),
            "expected_cost_m": float((mu * severity).sum()),
            "efficacy_alpha": 3.5,
            "efficacy_beta": 8.0,
            "efficacy_mean_pct": 100 * 3.5 / 11.5,
            "simulations": n,
            "reference": reference,
            "backtest": {
                "predicted_total_2025": float(backtest["predicted25"].sum()),
                "actual_total_2025": int(backtest["x25"].sum()),
                "error_pct": 100 * (backtest["predicted25"].sum() / backtest["x25"].sum() - 1),
                "segments": [
                    {
                        "segment": s,
                        "predicted": float(backtest.loc[s, "predicted25"]),
                        "actual": int(backtest.loc[s, "x25"]),
                    }
                    for s in SEGS
                ],
            },
        },
        "hiring": {
            "agency_hires_2y": len(agency_window),
            "agency_hires_pa": len(agency_window) / YEARS,
            "average_agency_fee": float(agency_window["fee"].mean()),
            "direct_benchmark": DIRECT_COST,
            "fee_ratio": float(agency_window["fee"].mean() / DIRECT_COST),
            "premium_pa_m": agency_premium_pa,
            "premium_per_hire": float(agency_window["premium"].mean()),
            "matched_strata": len(both),
            "matched_employees": len(matched),
            "agency_matched_early_pct": 100 * float(matched_channel.loc["agency", "early"]),
            "direct_matched_early_pct": 100 * float(matched_channel.loc["direct", "early"]),
            "agency_matched_days": float(matched_channel.loc["agency", "days"]),
            "direct_matched_days": float(matched_channel.loc["direct", "days"]),
            "shift_savings": [
                {
                    "shift_pct": share,
                    "hires_shifted": len(agency_window) / YEARS * share / 100,
                    "gross_savings_m": len(agency_window) / YEARS * share / 100 * agency_window["premium"].mean() / 1e6,
                }
                for share in [25, 50, 75]
            ],
        },
        "radar": {
            "senior_active_hipos": int((active["hipo_flag"] & (active["role_level"] >= 3)).sum()),
        },
        "decisions_not_modelled": [
            {"decision": "Fix the measurement rule", "reason": "A prerequisite that improves visibility; it does not itself prevent exits."},
            {"decision": "Run the senior HiPo Radar", "reason": "Review 119 senior active HiPos quarterly as a value-based operating list; do not turn it into a predictive score or publish named data."},
            {"decision": "Do not build employee flight-risk scores", "reason": "Engagement adds no usable individual warning for the target population."},
            {"decision": "Do not fund residual churn", "reason": f"The residual A${annual_cost_m(residual):.1f}M has no shared observed mechanism."},
            {"decision": "Re-base disengagement", "reason": "The 15% productivity multiplier is roughly 25× the observed goal-score gap."},
            {"decision": "Treat direct sourcing separately", "reason": "It is a hiring-cost lever, not part of the retention scenario."},
        ],
    }

    # Final-standard reconciliation gates.
    assert len(headline) == 341
    assert round(bucket1, 1) == 27.5
    assert round(bucket1 + bucket2 + bucket3, 1) == 45.9
    assert (tp, fn, fp) == (118, 223, 35)
    assert round(annual_cost_m(driver_union), 1) == 15.8
    assert round(rr, 2) == 3.36
    assert round(float((mu * severity).sum()), 1) == 29.0
    assert round(reference["NONE"]["median_m"], 1) == 28.9
    assert round(reference["C+D+E"]["median_m"], 1) == 28.0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(round_tree(snapshot), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {output}")
    print("Reconciled 341 exits | A$27.5M/year | A$15.8M driver union | A$28.0M portfolio median")


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    default_raw = project.parent / "upload"
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=default_raw)
    parser.add_argument("--notebook", type=Path, default=default_raw / "NovaCorp_Story(1).ipynb")
    parser.add_argument("--output", type=Path, default=project / "data" / "final_snapshot.json")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(args.raw_dir, args.notebook, args.output)
