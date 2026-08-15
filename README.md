# NovaCorp Decision Lab

[Open the live dashboard](https://accenturedashboard-novacorp.streamlit.app/)

NovaCorp Decision Lab turns the finalized `NovaCorp_Story.ipynb` analysis into an executive decision tool. It helps HR leaders see the genuine regrettable-attrition problem, compare targeted interventions, and understand what could happen financially if NovaCorp acts—or does nothing.

> **See the loss correctly → isolate bounded drivers → price the available moves → compare action with status quo → pilot, measure, and scale only if results justify it.**

The dashboard is a cohort-level planning simulator. It is **not** an employee flight-risk model, and its scenario outputs are **not guaranteed savings**.

---

## The decision in one minute

| Question                                           |                                                                       Finalized evidence | Decision implication                                                         |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------- |
| What is the strongly supported retention problem?  |    **341 genuine regrettable exits over 24 months; A$27.5M annual replacement exposure** | Focus on employee-initiated, high-value departures—not all attrition.        |
| Can HR currently see it?                           |                               **34.6% recall; 223 target exits and A$17.8M/year missed** | Correct the measurement rule before adding predictive analytics.             |
| Where is action defensible?                        | **A$15.8M/year, or 57% of exposure, lies inside three de-duplicated structural drivers** | Use targeted, owner-led programmes rather than a generic retention campaign. |
| What happens under the finalized 2026 assumptions? |                                    **Status quo median A$28.91M; C+D+E median A$28.01M** | The portfolio is financially plausible, but uncertain.                       |
| How strong is the scenario evidence?               |                     **61.49% modeled probability that C+D+E costs less than status quo** | Pilot with comparison groups and stopping rules; do not promise savings.     |
| Where else can replacement cost be reduced?        |                                      **Agency fees are about 4.0× the Direct benchmark** | Test Direct sourcing separately from the retention model.                    |

The management message is simple:

> **Keep valuable people → avoid expensive replacement → hire more efficiently.**

---

## How the analysis reaches the recommendation

The dashboard follows five linked questions.

| Stage           | Business question                                 | What the analysis found                                                                                                       | What management should do                                                               |
| --------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **1. Define**   | Which exits are genuinely regrettable?            | Retention should target voluntary, employee-initiated pull exits involving an Outstanding performer, High Performer, or HiPo. | Use one consistent three-field definition.                                              |
| **2. Measure**  | Does the current HR flag detect that population?  | It catches only 118 of 341 target exits and misses A$17.8M/year.                                                              | Fix detection and record reconciliation first.                                          |
| **3. Diagnose** | Is there a reliable individual warning signal?    | Engagement did not validate an employee-level leaver signal.                                                                  | Fix cohort conditions; do not score employees.                                          |
| **4. Bound**    | Where is there a plausible, actionable mechanism? | HiPo career friction, integration timing, and senior R&C pressure form three bounded drivers.                                 | Assign a specific intervention and owner to each driver.                                |
| **5. Decide**   | Which moves are affordable and worth testing?     | C, D, and E have finite costs and attainable break-even thresholds; blanket pay and promotion do not.                         | Pilot, observe actual efficacy, and scale only after financial and fairness gates pass. |

This is the logic behind every dashboard view:

> **Finding → Evidence → Boundary → Action → Test**

---

## What counts as genuine regrettable attrition

NovaCorp recorded 1,133 voluntary exits during CY2024–CY2025. However, 688—approximately 61%—were employer-initiated `push` exits. They are not the same retention problem as valuable employees choosing to leave.

The finalized target is:

```text
Voluntary exit
AND employee-initiated pull pathway
AND (Outstanding OR High Performer OR HiPo)
```

This definition identifies **341 exits over 24 months**.

For every target exit, replacement exposure is calculated using the case convention:

```text
Replacement exposure per exit
= salary at exit × 1.5 replacement multiplier × 85% backfill rate
```

The 24-month employee-level costs are summed and divided by two, producing approximately **A$27.5M in annual replacement exposure**.

This is an exposure estimate: the cost associated with replacing the observed leavers. It is not proof that any employee attribute caused the cost, and it is not a guaranteed saving available to management.

---

## Why the analysis does not predict individual leavers

The finalized analysis found no reliable engagement-based warning signal for the target population:

* approximately **84%** of target leavers still answered their final pre-exit survey;
* their final score was only **0.12 standard deviations below average**;
* the difference from stayers was not statistically conclusive; and
* there was no meaningful within-person deterioration.

The visible disengagement signature was stronger among `push` exits, not the high-value `pull` exits NovaCorp wants to retain.

Therefore, the dashboard models **cohort-level conditions and costs**, not individual resignation probabilities. Engagement can support confidential, voluntary outreach, but must not be used for “likely leaver” labels, promotion decisions, discipline, or retention-budget rankings.

---

## How historical evidence becomes the 2026 status quo

The 2026 model first divides the 12,003 active employees into mutually exclusive segments in this order:

```text
HiPo → Entity B/C → Risk & Compliance → base
```

The priority rule means one employee appears in only one segment. This prevents double counting when interventions are combined.

| Mutually exclusive segment | Active headcount | Expected 2026 exits | Average replacement severity | Expected replacement exposure |
| -------------------------- | ---------------: | ------------------: | ---------------------------: | ----------------------------: |
| HiPo                       |            1,029 |                54.7 |            A$164.8k per exit |                       A$9.01M |
| Entity B/C                 |            2,311 |                38.1 |            A$152.4k per exit |                       A$5.81M |
| Risk & Compliance          |            1,280 |                15.0 |            A$180.1k per exit |                       A$2.69M |
| Base                       |            7,383 |                72.3 |            A$158.6k per exit |                      A$11.46M |
| **Total**                  |       **12,003** |           **180.0** |                            — |         **A$28.98M expected** |

The segment estimates are built as follows:

* **HiPo, R&C, and base:** blended CY2024–CY2025 exit rates applied to current active headcount.
* **Entity B/C:** a steady-state baseline of 22 exits plus a finalized 2026 integration pulse of 16.1 incremental exits.
* **Severity:** the mean observed salary-based replacement exposure for actual exits in each segment.
* **Expected segment cost:** projected exits × segment replacement severity.

The model is not saying that a HiPo flag, entity code, or department “caused” a specific dollar amount. Those indicators define bounded planning cohorts. The cost comes from actual salary-at-exit records and the common Finance replacement-cost convention.

The expected status-quo cost is A$28.98M. After Poisson uncertainty is simulated, the status-quo **median** is A$28.91M, with a 90% modeled range of A$25.47M–A$32.50M. The expected value and median are close but not identical because they summarize the distribution differently.

---

## Why C, D, and E are the simulator moves

C, D, and E are not arbitrary labels. They are the three retention designs that survive the finalized decision filters:

1. a bounded workforce condition is observed;
2. there is a plausible mechanism for action;
3. an accountable owner can act;
4. the reachable 2026 exposure can be estimated;
5. the programme has a defined annual cost;
6. break-even efficacy is below 100%;
7. the action can be tested as a bounded pilot; and
8. it does not require employee-level prediction.

| Move                                | What management would do                                                                                                                 | Annual programme cost |                      Reachable 2026 exposure | Break-even efficacy | Finalized decision                                   |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------: | -------------------------------------------: | ------------------: | ---------------------------------------------------- |
| **A — Blanket HiPo pay fix**        | Raise all 1,029 active HiPos to 0.95 compa-ratio.                                                                                        |              A$13.10M |                                      A$9.01M |              145.3% | Reject: impossible to break even.                    |
| **B — Blanket promotion**           | Promote all 311 eligible HiPos to 0.90 of the next-level band.                                                                           |              A$14.47M | Only about 27% of HiPo exposure is reachable |              602.1% | Reject: most spend falls outside reachable exposure. |
| **C — HiPo career programme**       | Progression criteria, structured career conversations, mobility and development options, plus 20 funded accelerated promotions per year. |               A$1.75M |                                      A$9.01M |               19.5% | Pilot.                                               |
| **D — Entity B milestone playbook** | Role clarity, milestone communications, and retention conversations before consolidation.                                                |               A$1.00M |                    A$2.46M integration pulse |               40.6% | Time-sensitive pilot.                                |
| **E — R&C FAR readiness**           | FAR-readiness support, accountability support, role clarity, and market benchmarking.                                                    |               A$0.60M |                                      A$2.69M |               22.3% | Pilot.                                               |

### Where the programme costs come from

* **C:** delivery support for 1,029 active HiPos at A$800 per person, plus the full salary and 12% superannuation cost of 20 accelerated promotions, producing A$1.753889M per year.
* **D:** the finalized A$1.0M annual planning budget for integration support, communications, and role clarity. It contains no blanket retention bonus.
* **E:** the finalized A$0.6M annual planning budget for division-wide FAR readiness and role clarity. A broader pay uplift is deliberately excluded.
* **A and B:** full salary adjustments plus 12% superannuation. Their high costs are why the arithmetic rejects them.

Break-even is calculated as:

```text
Break-even efficacy
= annual programme cost ÷ financially reachable exposure
```

For B, reachable exposure is also reduced by the approximately 27% coverage of promotion-eligible HiPo exits. An intervention requiring more than 100% efficacy cannot pay for itself even if it prevents every reachable exit.

---

## How to use the Strategy Simulator

### 1. Select one move or a combination

Switch C, D, and E on or off to compare:

* no intervention;
* each move independently;
* any pair of moves; or
* the full C+D+E portfolio.

This reveals whether a portfolio is being carried by one strong intervention or genuinely improved by combining moves.

Selected programmes contribute both their modeled benefit and their full annual cost. Unselected programmes contribute neither.

### 2. Choose the efficacy assumption

Efficacy means:

> **The share of exits financially reachable by a selected programme that the programme prevents.**

It does **not** mean a NovaCorp-wide attrition reduction.

The available presets are:

* **Conservative — 15%:** tests a weak pilot outcome;
* **Notebook prior — 30.4%:** reproduces the finalized mean assumption;
* **Strong — 45%:** tests a stronger outcome; and
* **Custom — 0% to 60%:** supports explicit sensitivity analysis.

The finalized uncertainty prior is Beta(3.5, 8), with a mean of 30.4%. In a custom scenario, the simulator moves the mean while retaining the same overall concentration. Efficacy remains an assumption until a controlled pilot measures it.

Why change it: efficacy is the most decision-sensitive unknown. Moving it shows the minimum performance a programme needs, the downside if delivery is weak, and the upside if implementation is stronger.

### 3. Use advanced assumptions only as stress tests

The advanced panel changes planning inputs; it never changes the finalized historical evidence.

| Control                                     | What it means                                                        | What it changes                                               | Why a client might change it                                                   |
| ------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Expected additional consolidation exits** | Incremental exits above the 22-exit Entity B/C steady-state baseline | Status-quo Entity B/C exposure and the portion reachable by D | Test a smaller or larger integration event than the finalized 16.1-exit pulse. |
| **C annual programme cost**                 | Budget required for the career programme                             | Programme spend, net value, total cost, and break-even        | Replace the planning estimate with a validated implementation budget.          |
| **D annual programme cost**                 | Budget required for the milestone playbook                           | Programme spend, net value, total cost, and break-even        | Test alternative event-support designs.                                        |
| **E annual programme cost**                 | Budget required for FAR readiness                                    | Programme spend, net value, total cost, and break-even        | Test a confirmed delivery budget without inventing a broader pay case.         |

Programme cost changes total cost one-for-one. It does not change expected exits. The pulse changes only integration exposure. It does not change the HiPo or R&C projections.

Use **Reset to notebook** before presenting the finalized decision case. Any changed input is correctly treated as a derived planning scenario rather than historical evidence.

**Reference-frame note:** in the current release, the large “Do nothing” card and dashed chart line remain the locked A$28.91M notebook benchmark. If the integration pulse is changed, the derived delta, break-even, probability, contribution table, and financial bridge use the altered pulse. For the clearest like-for-like presentation, leave the pulse at 16.1 exits and use other values only as documented stress tests.

---

## How the simulator calculates action scenarios

For each selected move, the model converts cohort scale into financially reachable exposure.

### Expected-value logic

```text
Expected avoided exits
= reachable exits × selected mean efficacy

Gross exposure avoided
= expected avoided exits × segment replacement severity

Expected net value
= gross exposure avoided − programme spend

Expected total cost after action
= status-quo expected replacement cost
  − gross exposure avoided
  + programme spend
```

At the finalized 30.4% mean efficacy:

| Move      |          Reachable exits | Expected avoided exits | Gross exposure avoided | Programme cost | Expected net value |
| --------- | -----------------------: | ---------------------: | ---------------------: | -------------: | -----------------: |
| C         |          54.7 HiPo exits |                   16.6 |                A$2.74M |        A$1.75M |        **A$0.99M** |
| D         |         16.1 pulse exits |                    4.9 |                A$0.75M |        A$1.00M |       **−A$0.25M** |
| E         |           15.0 R&C exits |                    4.6 |                A$0.82M |        A$0.60M |        **A$0.22M** |
| **C+D+E** | **85.8 reachable exits** |               **26.1** |            **A$4.31M** |    **A$3.35M** |        **A$0.96M** |

D is intentionally different from C and E:

```text
Entity B/C action intensity
= 22 steady-state exits
  + 16.1 pulse exits × (1 − efficacy)
```

D can reduce only the predicted integration pulse. It receives no credit for eliminating the 22-exit steady-state baseline.

### Monte Carlo logic

The dashboard runs 10,000 simulations.

For each run:

1. each segment’s exit count is drawn from a Poisson distribution around its projected intensity;
2. each selected programme receives an efficacy draw from the planning distribution;
3. the relevant segment or pulse intensity is reduced;
4. simulated exits are multiplied by segment replacement severity; and
5. selected programme costs are added with certainty.

In simplified form:

```text
Status-quo cost
= sum over segments [Poisson(expected exits) × segment severity]

Action cost
= sum over adjusted segments [Poisson(adjusted exits) × segment severity]
  + selected programme costs
```

When several moves are selected, their avoided exits, avoided exposure, and costs are combined across mutually exclusive segments. The simulator assumes **no synergy or spillover** between programmes. This keeps the comparison additive and prevents double counting.

The output is a distribution of possible annual costs—not a forecast of which employees will leave.

---

## How to read the simulator outputs

Read the Strategy Simulator from top to bottom.

### Source badge

* **Final notebook output:** the selected scenario and all inputs exactly match a scenario printed in `NovaCorp_Story.ipynb`.
* **Derived scenario output:** the user selected an unprinted combination or changed an assumption.

Derived does not mean invalid. It means conditional on user-selected assumptions rather than a locked notebook result.

### Do nothing versus take action

The two large panels compare the finalized status quo with the selected strategy.

* **Median cost:** the middle of the modeled annual-cost distribution.
* **90% modeled range:** the 5th to 95th percentile across simulations. This is a scenario range, not a causal confidence interval.
* **Difference from status quo:** the selected scenario median minus the comparable status-quo median.

### Decision metrics

* **Expected avoided exits:** average target exits prevented under the chosen efficacy.
* **Gross exposure avoided:** replacement exposure associated with those avoided exits, before programme cost.
* **Programme spend:** annual cost of all selected moves.
* **Expected net value:** gross exposure avoided minus programme spend.
* **Portfolio break-even:** common efficacy required for the selected combination’s expected gross benefit to equal its cost.
* **Probability cost is lower:** share of modeled action runs with lower total cost than the corresponding status-quo simulations under the stated assumptions.

A positive expected net value and a median below status quo indicate financial plausibility. They do not establish causal impact or guarantee realized savings.

### Contribution table

Use this table to see which move strengthens or weakens the portfolio at the chosen efficacy. It separates avoided exits, gross value, spend, expected net value, and individual break-even thresholds.

### Financial bridge

The bridge makes the accounting visible:

```text
Status-quo expected replacement cost
− gross exposure avoided
+ programme spend
= expected cost after action
```

This prevents “avoided exposure” from being mistaken for net savings.

### Combination comparison

The common-scale chart compares all eight C/D/E combinations.

* dot = median modeled cost;
* horizontal line = 90% modeled range;
* highlighted row = current selection; and
* dashed reference = finalized notebook status-quo median.

Pairwise combinations are model-derived planning outputs. They are based on the finalized segment assumptions but were not all printed as standalone notebook scenarios.

---

## What the finalized scenario says

| Scenario   | Median total 2026 cost | 90% modeled range | Difference from status quo | Probability cost is lower |
| ---------- | ---------------------: | ----------------: | -------------------------: | ------------------------: |
| Status quo |               A$28.91M | A$25.47M–A$32.50M |                          — |                         — |
| C only     |               A$27.98M | A$24.11M–A$31.94M |          **A$0.93M lower** |                    62.32% |
| D only     |               A$29.19M | A$25.74M–A$32.84M |         **A$0.28M higher** |                    45.89% |
| E only     |               A$28.69M | A$25.28M–A$32.31M |          **A$0.21M lower** |                    52.42% |
| C+D+E      |               A$28.01M | A$24.13M–A$31.89M |          **A$0.90M lower** |                    61.49% |

The correct management interpretation is:

* **C is the portfolio’s financial anchor.** It has the largest reachable exposure and clears break-even under the finalized mean assumption.
* **E is a smaller, financially plausible pilot.** Its evidence is triangulated, but the senior-rate estimate rests on five exits.
* **D does not clear standalone break-even at 30.4% efficacy.** It remains relevant because its risk is dated, its target is observable, and Entity A provides an internal operating precedent.
* **C+D+E beats status quo in the median but is not clearly better than C alone.** The full portfolio should therefore be treated as three accountable pilots, not one unquestioned rollout.
* **A$0.90M is not promised savings.** Costs are certain; benefits depend on exits that may or may not be prevented.

The simulator supports this recommendation:

> **Launch C as the financial anchor; run E as a bounded pilot; retain D only as a time-sensitive milestone pilot with explicit event and financial gates. Measure all three before scaling.**

If management prioritizes near-term replacement-cost evidence alone, it can begin with C, consider E, and hold D until the milestone design is agreed. If management prioritizes protection against the predicted integration event, D can remain a bounded A$1.0M pilot with a predeclared pulse target and stopping rule.

---

## Hiring efficiency is a separate lever

The Agency-to-Direct control is deliberately outside the retention simulation because it changes replacement efficiency, not employee retention.

The finalized inputs are:

* 137 Agency hires per year;
* average Agency fee A$22,161 per hire;
* Direct benchmark A$5,500 per hire; and
* gross premium A$16,661 per shifted hire.

The slider calculates:

```text
Gross premium addressed
= annual Agency hires × share shifted to Direct
  × (average Agency fee − Direct benchmark)
```

At a 50% shift:

```text
137 × 50% × A$16,661 ≈ A$1.14M gross premium addressed
```

This is not net savings. NovaCorp must still measure internal recruiter capacity, sourcing cost, fill rate, vacancy duration, candidate quality, 12-month retention, and diversity before scaling Direct-first hiring.

---

## How an HR leader should use the dashboard

### First: establish the problem

Open **Decision overview** and look for:

1. A$27.5M of genuine regrettable-attrition exposure;
2. A$17.8M currently invisible to HR; and
3. A$15.8M inside three de-duplicated structural drivers.

This moves the conversation from “attrition is high” to “valuable pull exits are expensive, incompletely detected, and partly concentrated in actionable cohorts.”

### Second: isolate the decision

Open **Strategy simulator**, reset to the notebook, and toggle C, D, and E one at a time. Then compare C with C+E and C+D+E.

Ask:

* Which move creates the most expected net value?
* Which move fails break-even at the current efficacy?
* Does combining moves materially improve the median?
* How much uncertainty remains?
* What efficacy would each pilot need to justify scaling?

### Third: stress-test the assumptions

Move efficacy from 15% to 30.4% to 45%. Change programme costs only when a better budget estimate exists. Change the integration pulse only to test a documented alternative event scenario.

The purpose is not to search for a favorable answer. It is to identify which assumption changes the decision and what the pilot must measure.

### Fourth: define the test before spending

Open **Evidence & controls** and pre-register:

* delivery measures;
* 365-day genuine regrettable pull-exit outcomes;
* a phased, randomized, or otherwise credible comparison group;
* actual programme cost;
* realized replacement exposure;
* scale and stop thresholds; and
* fairness checks for sufficiently large subgroups.

---

## What must be measured before scaling

| Pilot                        | Delivery evidence                                                                                           | Outcome evidence                                                               | Stop or hold if…                                                                  |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **C — Career progression**   | Career conversations, documented criteria, reassessment dates, mobility access, and 20 funded accelerations | 365-day high-value pull-exit rate, internal mobility, and promotion outcomes   | No credible retention improvement, implementation failure, or unfair access       |
| **D — Integration playbook** | Milestone communications, role clarity, and pre-event retention conversations                               | Excess exits around the predeclared event window versus the 16.1-exit pulse    | The event does not occur, the pulse is not reduced, or net value remains negative |
| **E — FAR readiness**        | Readiness completion, accountability support, and role clarity                                              | L4+ exit rate and confidence-in-role-future trend                              | No credible improvement or evidence remains too unstable                          |
| **Portfolio**                | Actual programme spend and delivery fidelity                                                                | Avoided replacement exposure and realized net value against a comparison group | Net value is not positive or uncertainty remains decision-changing                |
| **Fairness**                 | Selection and participation by sufficiently large subgroup                                                  | Access and outcome gaps                                                        | Any unacceptable fairness consequence emerges                                     |

This is how the simulator supports the recommendation: it identifies the financially material assumptions and thresholds; the pilot determines whether those assumptions are true.

---

## Important recommendations outside the simulator

Some decisions should not be represented as retention-effect sliders.

* **Fix the measurement rule:** using the three-field definition improves visibility; it does not itself prevent exits.
* **Repair exit-record reconciliation:** trustworthy historical labels are a prerequisite for future analytics.
* **Use engagement for supportive outreach only:** no employee ranking or disciplinary use.
* **Run the senior HiPo Radar:** review the 119 active Level 3+ HiPos as a value-based operating list, not a prediction list.
* **Re-base disengagement exposure:** A$13.1M reproduces Finance’s 15% productivity assumption; the observed goal-score gap supports only about A$0.53M and is statistically inconclusive.
* **Test Direct sourcing separately:** the A$1.14M at a 50% shift is gross addressable premium, not guaranteed net savings.
* **Do not fund residual churn generically:** the remaining A$11.7M has no shared observed mechanism.

---

## Evidence boundaries and responsible use

Use the dashboard for:

* cohort-level portfolio planning;
* comparing action with doing nothing;
* discussing break-even thresholds;
* selecting bounded pilots;
* pre-registering outcomes and stopping rules; and
* reviewing aggregate, sufficiently large groups.

Never use it for:

* employee flight-risk rankings or “likely leaver” labels;
* promotion, discipline, or manager-performance decisions;
* manager league tables or publication of cells below ten;
* claims that a department, manager, or employee attribute caused attrition;
* treating historical exposure or modeled benefit as guaranteed savings; or
* claiming programme efficacy before a controlled evaluation observes it.

The public dashboard uses an aggregate finalized snapshot. It contains no employee names, employee IDs, manager IDs, reviewer IDs, original row-level HR tables, or named Radar list.

---

## Thirty-second walkthrough

> Start on **Decision overview**: NovaCorp has A$27.5M in annual genuine regrettable-attrition exposure, and the current HR flag misses A$17.8M of it. Three de-duplicated structural drivers cover A$15.8M, which is why the recommendations target career progression, integration timing, and R&C readiness. Then open **Strategy simulator** and compare C, D, and E individually and together. The model shows both benefit and programme spend, so avoided exposure is never confused with net value. Under the finalized assumptions, C is the financial anchor, E is a smaller plausible pilot, and D is a time-sensitive test that does not clear standalone break-even at the default efficacy. Finally, use **Evidence & controls** to see what must be observed before scaling. The dashboard supports a controlled pilot decision; it does not predict employees or promise savings.
