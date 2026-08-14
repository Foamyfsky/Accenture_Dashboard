from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT))

from core.scenario import all_selections, selection_label, simulate


class DashboardContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.snapshot = json.loads((ROOT / "data" / "final_snapshot.json").read_text(encoding="utf-8"))

    def test_finalized_headline_reconciles(self) -> None:
        self.assertEqual(self.snapshot["finance"]["genuine_exits_2y"], 341)
        self.assertAlmostEqual(self.snapshot["finance"]["regrettable_m"], 27.525146, places=6)
        self.assertEqual(self.snapshot["measurement"]["tp"], 118)
        self.assertEqual(self.snapshot["measurement"]["fn"], 223)
        self.assertAlmostEqual(self.snapshot["measurement"]["missed_m"], 17.813344, places=6)

    def test_notebook_reference_is_locked(self) -> None:
        self.assertEqual(
            self.snapshot["metadata"]["notebook_sha256"],
            "4d6372ec6e4b93e8c6c9da9e723b65f421ab9f4d34470366e4dc28b0b7cc3068",
        )
        reference = self.snapshot["scenario"]["reference"]
        self.assertAlmostEqual(reference["NONE"]["median_m"], 28.907707, places=6)
        self.assertAlmostEqual(reference["C+D+E"]["median_m"], 28.005969, places=6)
        self.assertAlmostEqual(reference["C+D+E"]["difference_m"], -0.901737, places=6)
        self.assertAlmostEqual(reference["C+D+E"]["probability_lower_pct"], 61.49, places=2)

    def test_all_eight_strategy_combinations_run(self) -> None:
        keys = []
        for selected in all_selections():
            result = simulate(self.snapshot, selected, self.snapshot["scenario"]["efficacy_mean_pct"] / 100)
            keys.append(selection_label(selected))
            self.assertLessEqual(result.scenario_p05_m, result.scenario_median_m)
            self.assertLessEqual(result.scenario_median_m, result.scenario_p95_m)
        self.assertEqual(set(keys), {"NONE", "C", "D", "E", "C+D", "C+E", "D+E", "C+D+E"})

    def test_default_portfolio_expected_value_reconciles(self) -> None:
        result = simulate(self.snapshot, {"C", "D", "E"}, self.snapshot["scenario"]["efficacy_mean_pct"] / 100)
        self.assertAlmostEqual(result.programme_cost_m, 3.353889, places=6)
        self.assertAlmostEqual(result.gross_avoided_m, 4.311498, places=5)
        self.assertAlmostEqual(result.expected_net_value_m, 0.957609, places=5)
        self.assertAlmostEqual(result.expected_avoided_exits, 26.1, delta=0.1)

    def test_public_snapshot_contains_no_row_level_identifier_keys(self) -> None:
        forbidden = {"employee_id", "manager_id", "reviewer_id", "employee_name"}

        def visit(value) -> None:
            if isinstance(value, dict):
                self.assertTrue(forbidden.isdisjoint(value.keys()))
                for child in value.values():
                    visit(child)
            elif isinstance(value, list):
                for child in value:
                    visit(child)

        visit(self.snapshot)


if __name__ == "__main__":
    unittest.main()
