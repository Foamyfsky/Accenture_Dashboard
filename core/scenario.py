"""Scenario engine for C/D/E intervention combinations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations

import numpy as np


ACTION_CODES = ("C", "D", "E")


@dataclass(frozen=True)
class ScenarioResult:
    selection: str
    expected_exits_before: float
    expected_exits_after: float
    expected_avoided_exits: float
    baseline_expected_cost_m: float
    gross_avoided_m: float
    programme_cost_m: float
    expected_after_cost_m: float
    expected_net_value_m: float
    break_even_pct: float | None
    gross_return_per_dollar: float | None
    status_p05_m: float
    status_median_m: float
    status_p95_m: float
    scenario_p05_m: float
    scenario_median_m: float
    scenario_p95_m: float
    median_difference_m: float
    probability_lower_pct: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def selection_label(selected: set[str]) -> str:
    return "+".join(code for code in ACTION_CODES if code in selected) if selected else "NONE"


def all_selections() -> list[set[str]]:
    values: list[set[str]] = [set()]
    for size in range(1, len(ACTION_CODES) + 1):
        values.extend(set(group) for group in combinations(ACTION_CODES, size))
    return values


def simulate(
    snapshot: dict,
    selected: set[str],
    efficacy_mean: float,
    pulse_exits: float | None = None,
    costs: dict[str, float] | None = None,
    n: int = 10_000,
    seed: int = 42,
) -> ScenarioResult:
    scenario = snapshot["scenario"]
    segments = {row["segment"]: row for row in scenario["segments"]}
    interventions = {row["code"]: row for row in snapshot["interventions"]}
    selected = set(selected) & set(ACTION_CODES)
    pulse = scenario["entity_pulse_exits"] if pulse_exits is None else float(pulse_exits)
    entity_base = float(scenario["entity_baseline_exits"])
    mu = {name: float(row["expected_exits"]) for name, row in segments.items()}
    mu["Entity_B/C"] = entity_base + pulse
    severity = {name: float(row["severity_m"]) for name, row in segments.items()}
    action_cost = {
        code: float((costs or {}).get(code, interventions[code]["cost_m"])) for code in ACTION_CODES
    }

    concentration = float(scenario["efficacy_alpha"] + scenario["efficacy_beta"])
    mean = min(max(float(efficacy_mean), 0.001), 0.999)
    alpha, beta = mean * concentration, (1 - mean) * concentration
    rng = np.random.default_rng(seed)
    status = sum(rng.poisson(mu[seg], n) * severity[seg] for seg in segments)

    if not selected:
        p05, median, p95 = np.percentile(status, [5, 50, 95])
        return ScenarioResult(
            selection="NONE",
            expected_exits_before=sum(mu.values()),
            expected_exits_after=sum(mu.values()),
            expected_avoided_exits=0.0,
            baseline_expected_cost_m=sum(mu[s] * severity[s] for s in segments),
            gross_avoided_m=0.0,
            programme_cost_m=0.0,
            expected_after_cost_m=sum(mu[s] * severity[s] for s in segments),
            expected_net_value_m=0.0,
            break_even_pct=None,
            gross_return_per_dollar=None,
            status_p05_m=float(p05),
            status_median_m=float(median),
            status_p95_m=float(p95),
            scenario_p05_m=float(p05),
            scenario_median_m=float(median),
            scenario_p95_m=float(p95),
            median_difference_m=0.0,
            probability_lower_pct=None,
        )

    arrays = {seg: np.full(n, mu[seg]) for seg in segments}
    expected_avoided = 0.0
    gross_avoided = 0.0
    addressable = 0.0

    if "C" in selected:
        effect = rng.beta(alpha, beta, n)
        arrays["HiPo"] = mu["HiPo"] * (1 - effect)
        expected_avoided += mu["HiPo"] * mean
        gross_avoided += mu["HiPo"] * severity["HiPo"] * mean
        addressable += mu["HiPo"] * severity["HiPo"]
    if "D" in selected:
        effect = rng.beta(alpha, beta, n)
        arrays["Entity_B/C"] = entity_base + pulse * (1 - effect)
        expected_avoided += pulse * mean
        gross_avoided += pulse * severity["Entity_B/C"] * mean
        addressable += pulse * severity["Entity_B/C"]
    if "E" in selected:
        effect = rng.beta(alpha, beta, n)
        arrays["R&C"] = mu["R&C"] * (1 - effect)
        expected_avoided += mu["R&C"] * mean
        gross_avoided += mu["R&C"] * severity["R&C"] * mean
        addressable += mu["R&C"] * severity["R&C"]

    programme_cost = sum(action_cost[code] for code in selected)
    draw = sum(rng.poisson(arrays[seg], n) * severity[seg] for seg in segments) + programme_cost
    status_p05, status_median, status_p95 = np.percentile(status, [5, 50, 95])
    p05, median, p95 = np.percentile(draw, [5, 50, 95])
    baseline_expected = sum(mu[s] * severity[s] for s in segments)
    expected_after = baseline_expected - gross_avoided + programme_cost

    return ScenarioResult(
        selection=selection_label(selected),
        expected_exits_before=sum(mu.values()),
        expected_exits_after=sum(mu.values()) - expected_avoided,
        expected_avoided_exits=expected_avoided,
        baseline_expected_cost_m=baseline_expected,
        gross_avoided_m=gross_avoided,
        programme_cost_m=programme_cost,
        expected_after_cost_m=expected_after,
        expected_net_value_m=gross_avoided - programme_cost,
        break_even_pct=100 * programme_cost / addressable if addressable else None,
        gross_return_per_dollar=gross_avoided / programme_cost if programme_cost else None,
        status_p05_m=float(status_p05),
        status_median_m=float(status_median),
        status_p95_m=float(status_p95),
        scenario_p05_m=float(p05),
        scenario_median_m=float(median),
        scenario_p95_m=float(p95),
        median_difference_m=float(median - status_median),
        probability_lower_pct=float(100 * (draw < status).mean()),
    )


def marginal_effects(snapshot: dict, efficacy_mean: float, pulse_exits: float, costs: dict[str, float]) -> list[dict]:
    scenario = snapshot["scenario"]
    segments = {row["segment"]: row for row in scenario["segments"]}
    entity_base = float(scenario["entity_baseline_exits"])
    del entity_base  # Included for semantic clarity; D only reaches the pulse.
    intervention = {row["code"]: row for row in snapshot["interventions"]}
    target_exits = {
        "C": float(segments["HiPo"]["expected_exits"]),
        "D": float(pulse_exits),
        "E": float(segments["R&C"]["expected_exits"]),
    }
    severity = {
        "C": float(segments["HiPo"]["severity_m"]),
        "D": float(segments["Entity_B/C"]["severity_m"]),
        "E": float(segments["R&C"]["severity_m"]),
    }
    rows = []
    for code in ACTION_CODES:
        avoided = target_exits[code] * efficacy_mean
        gross = avoided * severity[code]
        cost = float(costs.get(code, intervention[code]["cost_m"]))
        addressable = target_exits[code] * severity[code]
        rows.append(
            {
                "code": code,
                "name": intervention[code]["short_name"],
                "expected_avoided_exits": avoided,
                "gross_avoided_m": gross,
                "cost_m": cost,
                "net_m": gross - cost,
                "break_even_pct": 100 * cost / addressable,
            }
        )
    return rows
