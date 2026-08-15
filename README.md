# NovaCorp Decision Lab

[Open the live dashboard](https://accenturedashboard-novacorp.streamlit.app/)

NovaCorp Decision Lab is the interactive companion to the finalized Accenture × SUBAA Datathon presentation, **“Paying for exits you never chose.”** It translates the same evidence and recommendation into a tool that lets an HR leader compare doing nothing with one or more targeted programmes.

> **Separate the exits NovaCorp chose from the exits it would want back → find the groups where loss is persistent or event-driven → price the response → test it for 12 months → scale only what works.**

All monetary values are in Australian dollars. The tool models workforce cohorts and programme economics. It does **not** predict which employee will leave, prove that an observed factor caused attrition, or promise savings.

---

## The finalized recommendation

NovaCorp reports approximately **A$42M in annual people cost**. The analysis narrows that broad problem to the largest strongly supported and preventable component:

* **341 genuine regrettable exits over CY2024–CY2025**;
* **A$27.5M in annual replacement exposure**;
* **65% of those valuable exits missed by HR’s current flag**;
* **57% of the loss located inside three de-duplicated structural groups**; and
* **A$3.4M of targeted programmes** designed to address those groups.

The final management decision is:

> **Start with Career Progression for high-potentials. Run the Integration Plan and FAR Support Plan only against their specific risks. Treat year one as a test, not a rollout.**

Why Career Progression comes first:

* high-potentials are only about **9% of the workforce**;
* their exit rate is approximately **3.36×** that of other employees;
* the difference persists across every tenure band;
* the cohort carries approximately **A$8.7M in annual historical exposure**; and
* the programme costs about **A$1.8M**, requiring only **19% efficacy** to break even.

---

## How the dashboard follows the slide narrative

| Final deck question                     | What the slides establish                                                                                                                                               | Where to use it in the dashboard                  |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| **1. What is really costing NovaCorp?** | The 10.4% voluntary rate mixes 688 managed `push` exits with 445 employee-initiated `pull` exits. The genuine target is 341 valuable pull exits worth A$27.5M per year. | **Decision overview**                             |
| **Can HR see the target?**              | The current flag catches 118 exits and misses 223. Recall is only 34.6%.                                                                                                | **Decision overview** and **Evidence & controls** |
| **Can surveys predict who will leave?** | No reliable individual warning signal was validated. Target leavers still responded at approximately the same rate as stayers.                                          | **Decision overview** and **Evidence map**        |
| **2. Where is the loss?**               | High-potentials, integration-exposed employees, and R&C each show a different pattern requiring a different response.                                                   | Driver cards on **Decision overview**             |
| **Can group rates support planning?**   | The 2024-to-2025 backtest works reasonably for structural cohorts; the Entity B/C miss shows why integration must be modeled as an event.                               | **Evidence & controls**                           |
| **3. What if NovaCorp acts?**           | Blanket pay and promotion fail the arithmetic. Career Progression, Integration, and FAR support can be tested at finite cost.                                           | **Strategy simulator**                            |
| **What would justify scaling?**         | Delivery, exits, financial value, and fairness must pass predeclared gates.                                                                                             | **Pilot scorecard**                               |

The dashboard extends the deck without changing its conclusion. The slides communicate the decision simply; the simulator exposes the assumptions, uncertainty, and trade-offs behind it.

---

## 1. What is really costing NovaCorp?

### The headline attrition rate mixes two different events

NovaCorp recorded **1,133 voluntary exits** during CY2024–CY2025, but pathway data show:

| Pathway | Exits | Share | Meaning                                      |
| ------- | ----: | ----: | -------------------------------------------- |
| `push`  |   688 |   61% | Organisation-initiated or managed exits      |
| `pull`  |   445 |   39% | Employees leaving for an outside opportunity |

The board’s 10.4% voluntary rate therefore cannot be treated as one retention outcome. A lower rate could result from managing out fewer employees without retaining a single valuable employee.

### The finalized target isolates loss NovaCorp did not choose

```text
Genuine regrettable exit
= voluntary exit
  AND employee-initiated pull pathway
  AND (Outstanding OR High Performer OR HiPo)
```

This produces **341 exits over two years**.

Replacement exposure for each exit is calculated as:

```text
salary at exit × 1.5 replacement multiplier × 85% backfill rate
```

The two-year total is divided by two, producing **A$27.5M in annual replacement exposure**.

This is the central cost used by the retention story. It is an estimate of replacement exposure—not a claim that every dollar can be saved.

### Why the deck says A$42M while the dashboard also shows A$45.9M

* **A$42M** is Finance’s reported top-down people-cost estimate and is the context used by the presentation.
* Rebuilding the three supplied buckets produces approximately **A$45.9M**: A$27.5M attrition, A$13.1M disengagement under Finance’s 15% productivity assumption, and A$5.25M hiring cost.
* The difference does not change the recommendation because only the **A$27.5M regrettable-attrition component** is both strongly reconciled and central to the retention programmes.

The dashboard shows the reconciliation for transparency. The deck correctly leads with the reported A$42M and then narrows to the A$27.5M decision problem.

---

## 2. Fix what HR can see before adding prediction

The current regrettable-exit flag identifies:

* **118 true target exits**;
* **223 target exits it misses**; and
* **35 flagged exits that do not meet the finalized definition**.

This produces:

* **34.6% recall**;
* **77.1% precision**;
* **A$9.7M/year visible to the current process**; and
* **A$17.8M/year invisible to it**.

The current flag captures 64% of Outstanding leavers but only 8% of High Performers. Because High Performers are the larger group, most valuable loss is missed.

NovaCorp should replace the flag with the finalized three-field definition. This requires no new retention-programme budget, although annual case review rises from approximately **76 to 170 cases**.

This is a measurement correction—not an employee prediction model and not, by itself, a retention intervention.

---

## 3. Why the strategy targets groups rather than individuals

Survey responses did not identify who would leave:

* **84%** of genuine regrettable leavers responded to their last pre-exit survey;
* **80%** of stayers responded;
* `push` exits responded at only **54%**; and
* target leavers showed no meaningful pre-exit engagement decline.

Low response therefore signals something different—mainly managed exits—not the high-value pull loss NovaCorp wants to prevent.

The strategy does not ask, “Who will resign?” It asks:

> **Which groups carry stable or event-timed exposure, and what condition can management change?**

The backtest supports this level of planning:

| Cohort            | Predicted 2025 exits from 2024 rates | Actual 2025 exits | Interpretation                                                                 |
| ----------------- | -----------------------------------: | ----------------: | ------------------------------------------------------------------------------ |
| High-potentials   |                                   57 |                52 | Structural cohort rate transferred reasonably well.                            |
| Entity B/C        |                                   53 |                37 | Carrying a shock year forward over-predicted; integration must be event-timed. |
| Risk & Compliance |                                   14 |                16 | Cohort projection was close.                                                   |
| Other employees   |                                   76 |                69 | Base projection was reasonably close.                                          |

This validates cohort-level planning—not individual prediction and not causal programme efficacy.

---

## 4. Where the loss sits

### Driver 1 — High-potential career friction

* approximately **9% of the workforce**;
* **3.36×** the exit rate of other employees;
* 95% confidence interval **2.60–4.35**;
* the difference persists within every tenure band;
* average compa-ratio **0.88**; and
* approximately **A$8.7M/year historical exposure**.

For the driver test, HiPo status was kept out of the outcome definition to avoid a circular result. The evidence supports a persistent cohort problem, but it does not prove that pay causes exits. HiPos who stay are similarly below midpoint.

Supported response: **Career Progression**, not blanket pay.

### Driver 2 — Integration risk on a calendar

The deck identifies **2,521 employees** facing the broader integration transition. Like-for-like first-year rates show:

* Entity C: approximately **4.5 exits per 100 person-years**;
* NovaCorp comparable new hires: approximately **3.0**; and
* Entity B: approximately **2.6**.

Entity C is about 1.5× the comparable benchmark. Entity B’s raw exit count is large mainly because the cohort is large; it is not evidence of a permanently high underlying rate.

There is no pre-migration employee history, so the data cannot prove that integration caused the difference. The actionable point is that NovaCorp knows the timing of the upcoming milestone and can manage it prospectively.

Supported response: a bounded **Integration Plan** before the milestone.

### Driver 3 — Risk & Compliance pressure

* senior exit rate approximately **4.2 per 100 person-years**, the highest in NovaCorp;
* **five of five** engagement waves below the firm average for confidence in role futures; and
* approximately **A$5.9M/year historical exposure**.

The senior-rate result rests on five exits. It is supported by triangulation across attrition, survey evidence, and the Annual Report—not by sample size alone.

Supported response: **FAR Support and role clarity**.

### Why the driver figures must not be added directly

The descriptive driver groups overlap. An employee can be a HiPo, belong to Entity B/C, and work in R&C.

After de-duplication:

* **193 exits** sit inside at least one driver;
* they represent **A$15.8M/year**;
* this equals approximately **57% of the A$27.5M problem**; and
* the remaining **148 exits and A$11.7M/year** show no shared mechanism.

The recommendation does not fund a generic programme against the residual loss. A programme without a mechanism is spending without a testable thesis.

---

## 5. Why these three programmes—and not blanket pay or promotion

The analysis prices each design before recommending it.

| Option                      | Annual cost |                                   Financially reachable exposure | Break-even efficacy | Decision             |
| --------------------------- | ----------: | ---------------------------------------------------------------: | ------------------: | -------------------- |
| Blanket HiPo pay adjustment |     A$13.1M |                                                           A$9.0M |                145% | Impossible           |
| Promote every eligible HiPo |     A$14.5M |                                  Only about 27% of HiPo exposure |                602% | Impossible           |
| **C — Career Progression**  |  **A$1.8M** | **A$9.0M in the 2026 simulator; A$8.7M historical slide figure** |             **19%** | Pilot first          |
| **D — Integration Plan**    |  **A$1.0M** |                                  **A$2.5M event-pulse exposure** |             **41%** | Time-sensitive pilot |
| **E — FAR Support Plan**    |  **A$0.6M** |                                         **A$2.7M 2026 exposure** |             **22%** | Bounded pilot        |

Break-even is:

```text
annual programme cost ÷ financially reachable exposure
```

An intervention requiring more than 100% efficacy cannot recover its cost even if it prevents every financially reachable exit. That is why A and B are rejected by arithmetic rather than managerial preference.

### The A$3.4M action portfolio

The exact simulator cost is A$3.353889M, presented as **A$3.4M** in the deck:

* **Career Progression — A$1.8M:** clear criteria, career conversations, mobility and development options, plus 20 funded accelerated promotions per year;
* **Integration Plan — A$1.0M:** clearer roles, milestone communications, and retention conversations before integration; and
* **FAR Support Plan — A$0.6M:** FAR readiness, accountability support, and role clarity for R&C leaders.

The deck proposes funding these pilots through the existing People Reinvention budget. That means **no additional funding request**, not that the programmes are cost-free. Their A$3.4M opportunity cost remains inside every scenario.

Relative to Finance’s A$42M headline, A$3.4M is approximately **8% of annual people cost**. The decision is therefore to use a bounded first year to learn which programmes work before committing to scale.

### Why the deck says A$13.9M targeted while the simulator uses A$14.2M

The deck uses rounded communication figures:

```text
A$8.7M HiPo historical exposure
+ A$2.5M integration-pulse exposure
+ A$2.7M R&C exposure
= A$13.9M
```

The simulator uses exact, mutually exclusive 2026 inputs:

```text
A$9.013754M Career Progression exposure
+ A$2.460401M Integration Plan exposure
+ A$2.692193M FAR Support exposure
= A$14.166348M
```

These are different views of the same decision. The slides use rounded historical and event figures to explain the story; the simulator uses exact 2026 cohort projections to calculate outcomes.

### Two explanations the analysis does not use

* **Blanket pay:** within each performance tier, leaver and stayer compa-ratios are almost identical. HiPos sit below midpoint, but those who stay do too. Pay may be part of career friction, but it does not explain who leaves and cannot justify a blanket adjustment.
* **Manager hotspots:** 341 exits are spread across 328 managers, with only 13 managers recording two exits. The clustering test gives p=0.97, but the median span of control is only two. The responsible conclusion is that manager effects are not testable with these data—not that every manager is cleared. No manager should be ranked.

---

## 6. How the 2026 simulator baseline is built

To prevent double counting, the 12,003 active employees are assigned to one scenario segment in priority order:

```text
HiPo → Entity B/C → Risk & Compliance → base
```

| Mutually exclusive scenario segment | Active headcount | Expected 2026 exits | Mean replacement severity |     Expected exposure |
| ----------------------------------- | ---------------: | ------------------: | ------------------------: | --------------------: |
| HiPo                                |            1,029 |                54.7 |         A$164.8k per exit |               A$9.01M |
| Entity B/C                          |            2,311 |                38.1 |         A$152.4k per exit |               A$5.81M |
| Risk & Compliance                   |            1,280 |                15.0 |         A$180.1k per exit |               A$2.69M |
| Base                                |            7,383 |                72.3 |         A$158.6k per exit |              A$11.46M |
| **Total**                           |       **12,003** |           **180.0** |                         — | **A$28.98M expected** |

The deck’s 2,521 integration figure describes the broader affected population. The simulator’s 2,311 Entity B/C segment is smaller because overlapping HiPos are assigned to the HiPo segment first. This is how the combined simulation avoids counting the same person twice.

The baseline uses:

* blended CY2024–CY2025 rates for HiPo, R&C, and base;
* a 22-exit Entity B/C steady-state baseline;
* a **16.1-exit** incremental integration pulse;
* mean salary-based replacement severity for each segment; and
* 10,000 Poisson simulations for exit-count uncertainty.

The status-quo expected value is A$28.98M. Its simulated median is **A$28.91M**, with a 90% modeled range of **A$25.47M–A$32.50M**.

---

## 7. How to use the Strategy Simulator

### Step 1 — Select the move

Toggle C, D, and E on or off to compare:

* doing nothing;
* Career Progression alone;
* Integration alone;
* FAR Support alone;
* any pair; or
* all three programmes.

This makes the final recommendation visible: compare C with C+E and C+D+E to see whether adding a programme improves the portfolio or only adds cost.

### Step 2 — Choose programme efficacy

Efficacy means:

> **The percentage of financially reachable exits prevented by each selected programme.**

It is not a NovaCorp-wide attrition reduction.

| Setting                    | Question it answers                               |
| -------------------------- | ------------------------------------------------- |
| **15% — Conservative**     | What happens if implementation is weak?           |
| **30.4% — Notebook prior** | What happens under the finalized mean assumption? |
| **45% — Strong**           | What happens if delivery performs well?           |
| **Custom**                 | At what efficacy does the decision change?        |

The finalized uncertainty prior is Beta(3.5, 8), with a 30.4% mean. A custom value changes the centre of the distribution while retaining the same overall concentration.

This is the most important control because no historical dataset can reveal future programme efficacy. The purpose of the pilot is to measure it.

### Step 3 — Use advanced assumptions as documented stress tests

| Control                                     | Meaning                                                 | Financial effect                                                                                  |
| ------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Expected additional consolidation exits** | Incremental exits above the 22-exit Entity B/C baseline | Changes status-quo integration exposure and the portion D can address. It does not change C or E. |
| **C annual programme cost**                 | Validated delivery budget for Career Progression        | Adds one-for-one to selected programme spend and raises or lowers break-even.                     |
| **D annual programme cost**                 | Validated budget for Integration support                | Adds one-for-one to spend; it does not change expected exits.                                     |
| **E annual programme cost**                 | Validated budget for FAR Support                        | Adds one-for-one to spend; it does not change expected exits.                                     |

Use **Reset to notebook** before presenting the finalized case.

**Current-interface note:** the large “Do nothing” card and dashed reference line remain fixed at the notebook’s A$28.91M status-quo benchmark. If the integration pulse is changed, the derived delta, probability, break-even, contribution table, and financial bridge use the altered pulse. Leave the pulse at 16.1 exits for the clearest like-for-like presentation; use other values only as stress tests.

---

## 8. How costs and benefits are calculated

### Expected-value calculation

```text
Expected avoided exits
= financially reachable exits × mean efficacy

Gross exposure avoided
= expected avoided exits × segment replacement severity

Expected net value
= gross exposure avoided − selected programme costs

Expected total cost after action
= status-quo expected replacement cost
  − gross exposure avoided
  + selected programme costs
```

For C and E, the selected efficacy reduces the full projected target-segment intensity.

D is narrower:

```text
Entity B/C exits after D
= 22 steady-state exits
  + 16.1 pulse exits × (1 − efficacy)
```

The Integration Plan receives credit only for reducing the predicted event pulse. It does not receive credit for eliminating normal Entity B/C turnover.

### What the A$3.4M portfolio generates

The deck communicates the sensitivity in rounded terms:

| Mean efficacy | Gross exposure avoided | Programme cost |     Approximate net position | Decision reading                |
| ------------- | ---------------------: | -------------: | ---------------------------: | ------------------------------- |
| 15%           |                 A$2.1M |         A$3.4M |                  **−A$1.3M** | Below break-even; do not scale. |
| 30%           |                 A$4.2M |         A$3.4M | **about +A$0.8M to +A$0.9M** | Financially plausible; test.    |
| 45%           |                 A$6.4M |         A$3.4M |            **about +A$3.0M** | Stronger case, if observed.     |

At the dashboard’s exact 30.4% mean:

| Programme          | Expected avoided exits | Gross exposure avoided |        Cost | Expected net value |
| ------------------ | ---------------------: | ---------------------: | ----------: | -----------------: |
| Career Progression |                   16.6 |                A$2.74M |     A$1.75M |       **+A$0.99M** |
| Integration Plan   |                    4.9 |                A$0.75M |     A$1.00M |       **−A$0.25M** |
| FAR Support Plan   |                    4.6 |                A$0.82M |     A$0.60M |       **+A$0.22M** |
| **C+D+E**          |               **26.1** |            **A$4.31M** | **A$3.35M** |       **+A$0.96M** |

The expected-value result explains the deck’s recommendation:

* Career Progression carries the portfolio;
* FAR Support is modestly positive under the default assumption; and
* Integration is below standalone break-even at 30.4% and should remain a time-specific pilot.

The appendix also tests replacement multipliers, backfill rates, superannuation, programme cost, and integration-pulse size. Programme efficacy produces the widest decision swing and is the only major input the historical files cannot supply. At the 15% efficacy floor, portfolio net value becomes negative. This is why the recommendation is a staged pilot rather than a full rollout.

### Monte Carlo calculation

The dashboard then adds uncertainty through 10,000 simulations.

For each run:

1. segment exits are drawn from Poisson distributions around projected cohort intensities;
2. each selected programme receives an efficacy draw;
3. the appropriate segment or event pulse is reduced;
4. simulated exits are multiplied by segment replacement severity; and
5. programme costs are added with certainty.

```text
Status-quo cost
= Σ [Poisson(segment exit intensity) × segment severity]

Action cost
= Σ [Poisson(adjusted segment intensity) × segment severity]
  + selected programme costs
```

Selected programmes operate on mutually exclusive scenario segments. Their costs and benefits are added without assuming synergy, spillover, or double counting.

---

## 9. How to read the simulator outputs

### Final notebook output versus derived scenario

* **Final notebook output:** the selected scenario and inputs exactly match a scenario printed in the finalized notebook.
* **Derived scenario output:** the user changed an assumption or selected a combination not printed as a standalone notebook scenario.

Derived outputs are valid planning calculations, but they are conditional on the selected assumptions.

### Core metrics

* **Median cost:** the middle of the simulated annual-cost distribution.
* **90% modeled range:** the 5th–95th percentile across simulations; it is not a causal confidence interval.
* **Expected avoided exits:** mean reachable exits prevented under the selected efficacy.
* **Gross exposure avoided:** replacement exposure before programme costs.
* **Programme spend:** full annual cost of all selected moves.
* **Expected net value:** gross exposure avoided minus programme spend.
* **Portfolio break-even:** common efficacy at which expected gross benefit equals selected programme cost.
* **Probability cost is lower:** share of modeled action runs costing less than the comparable status-quo runs under the assumptions.

### Financial bridge

```text
status-quo expected exposure
− gross exposure avoided
+ programme spend
= expected cost after action
```

This is the most important accounting view because it prevents addressable exposure from being presented as savings.

### Combination chart

* dot = median modeled cost;
* horizontal range = 90% modeled range;
* highlighted row = selected combination; and
* dashed line = finalized status-quo median.

Use the chart to compare C, C+E, and C+D+E on one scale. Pairwise combinations are derived planning outputs based on the finalized segment model.

---

## 10. What the finalized simulations mean

| Scenario                | Median total 2026 cost | 90% modeled range | Difference from status quo | Probability cost is lower |
| ----------------------- | ---------------------: | ----------------: | -------------------------: | ------------------------: |
| Status quo              |               A$28.91M | A$25.47M–A$32.50M |                          — |                         — |
| Career Progression only |               A$27.98M | A$24.11M–A$31.94M |          **A$0.93M lower** |                    62.32% |
| Integration Plan only   |               A$29.19M | A$25.74M–A$32.84M |         **A$0.28M higher** |                    45.89% |
| FAR Support only        |               A$28.69M | A$25.28M–A$32.31M |          **A$0.21M lower** |                    52.42% |
| C+D+E portfolio         |               A$28.01M | A$24.13M–A$31.89M |          **A$0.90M lower** |                    61.49% |

The correct interpretation is:

1. **Career Progression is the first investment.** It targets the strongest persistent risk and produces the strongest standalone financial result.
2. **FAR Support is a bounded secondary pilot.** It is financially plausible, but the evidence is based on triangulation and a small number of senior exits.
3. **Integration is strategic rather than financially dominant at the default efficacy.** Its value depends on acting before a dated event and reducing the 16.1-exit pulse.
4. **The full portfolio beats doing nothing in the median, but not with certainty.** A 61.49% probability of lower cost supports a test—not a savings commitment.
5. **C+D+E is not clearly better than C alone.** The three programmes should retain separate owners, measures, and stopping rules.

This is fully consistent with the final slide:

> **Prioritise Career Progression first, while the Integration and FAR programmes target their specific risks.**

---

## 11. How NovaCorp should measure success

| Programme              | Measurement point    | Continue if…                                                                           | Stop or hold if…                                                                           |
| ---------------------- | -------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Career Progression** | 12 months            | Genuine regrettable exits fall and internal progression rises                          | No credible improvement or eligibility/access is unfair                                    |
| **Integration Plan**   | Q2 2026 event window | Integration-related attrition falls below the predeclared 16-exit pulse                | Attrition remains unchanged or the predicted event does not materialise                    |
| **FAR Support Plan**   | 12 months            | Senior attrition falls and confidence in role futures improves                         | No credible improvement                                                                    |
| **Portfolio**          | 12 months            | Realised avoided exposure exceeds actual programme spend against a credible comparison | Net value is not positive or delivery is incomplete                                        |
| **Fairness**           | Every review         | Access and outcomes remain acceptable across sufficiently large groups                 | Access is unequal across gender, age, or background—even if aggregate results are positive |

The pilot should pre-register definitions, comparison groups, outcomes, programme costs, scale gates, kill criteria, and fairness safeguards before launch.

---

## 12. What the dashboard supports—and what it does not

### Supported decisions

* Correct the regrettable-exit definition before relying on advanced analytics.
* Focus on high-value `pull` loss rather than the undifferentiated voluntary rate.
* Use cohort-level planning instead of employee-level flight-risk scores.
* Prioritise Career Progression for HiPos.
* Use the Integration Plan only around the known milestone.
* Run FAR Support as a bounded, measurable programme.
* Reject blanket HiPo pay and promotion on break-even arithmetic.
* Treat efficacy as the critical unknown that year one must measure.

### Not established

* That any observed driver caused an employee to leave.
* That every HiPo is individually at risk.
* That engagement can identify likely leavers.
* That Entity B has a permanently elevated underlying rate.
* That a department or manager caused concentrated loss.
* That the modeled A$0.90M median improvement will be realised.
* That any programme should scale before future outcomes pass the agreed gates.

---

## Supplementary dashboard lever: Agency-to-Direct sourcing

The dashboard also contains an Agency-to-Direct sourcing control. This is retained as a supplementary replacement-efficiency analysis, but it is **not part of the finalized 15-slide retention recommendation** and is not included in the C/D/E scenario.

It estimates gross addressable Agency premium as:

```text
137 annual Agency hires
× share shifted to Direct
× (A$22,161 Agency fee − A$5,500 Direct benchmark)
```

At a 50% shift, this equals approximately **A$1.14M gross premium addressed**. It is not net savings: internal sourcing cost, capacity, fill rate, vacancy duration, quality, retention, and diversity must be measured separately.

---

## Responsible use

Use the dashboard for:

* executive problem framing;
* cohort-level portfolio planning;
* comparing action with doing nothing;
* break-even and sensitivity discussion;
* selecting bounded pilots; and
* defining measurement and stopping rules.

Never use it for:

* employee flight-risk rankings or “likely leaver” labels;
* promotion or disciplinary decisions;
* manager league tables;
* publication of cells below ten;
* causal claims unsupported by the data; or
* presenting exposure or scenario benefit as guaranteed savings.

The public dashboard uses aggregate finalized outputs only. It contains no employee names, employee IDs, manager IDs, reviewer IDs, original row-level HR tables, or named HiPo Radar list.

---

## Thirty-second walkthrough

> NovaCorp reports A$42M in annual people cost, but the first decision is to isolate the loss it did not choose: 341 genuine regrettable pull exits worth A$27.5M per year. HR’s current flag misses 65% of them, while surveys do not reliably identify who will leave. The evidence instead points to three different groups with three different mechanisms: persistent HiPo loss, a dated integration risk, and senior R&C pressure. The simulator shows why blanket pay and promotion are rejected and lets management compare the A$3.4M Career, Integration, and FAR programmes with doing nothing. At the finalized assumptions, Career Progression is the financial anchor; FAR is a smaller bounded pilot; and Integration must prove itself against the predicted event pulse. Year one is a test, not a rollout. Scale only if retention, financial value, delivery, and fairness all pass their predeclared gates.
