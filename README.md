# NovaCorp Decision Lab

[Open the live dashboard](https://accenturedashboard-novacorp.streamlit.app/)

An interactive decision-support tool that helps NovaCorp understand its genuine regrettable-attrition problem, compare targeted interventions, and evaluate what could happen financially if management acts—or does nothing.

The dashboard translates the finalized `NovaCorp_Story.ipynb` analysis into an executive workflow:

> **See the loss correctly → identify bounded structural drivers → compare affordable actions → pilot, measure, and scale only when the evidence justifies it.**

This is not an employee flight-risk model. It is a cohort-level planning tool for the CHRO, CFO, Talent & Reward, Integration Programme, Risk & Compliance leadership, and Talent Acquisition.

---

## Executive message

NovaCorp’s workforce-cost problem is not simply “high attrition.”

It is a combination of:

1. preventable loss of valuable employees;
2. an existing HR definition that misses much of that loss;
3. structural conditions that affect bounded workforce cohorts;
4. uncertain intervention efficacy that must be tested; and
5. expensive replacement hiring that compounds the cost.

The finalized analysis identifies:

| Executive finding             |                                                Finalized evidence | Management implication                                                                |
| ----------------------------- | ----------------------------------------------------------------: | ------------------------------------------------------------------------------------- |
| Genuine regrettable attrition | **341 exits over 24 months; A$27.5M annual replacement exposure** | Focus retention resources on employee-initiated, high-value departures                |
| Current detection gap         |        **34.6% recall; 223 target exits and A$17.8M/year missed** | Correct the measurement rule before building further analytics                        |
| Three bounded drivers         |         **A$15.8M/year, or 57% of exposure after de-duplication** | Fund interventions only where there is a plausible mechanism                          |
| Status quo 2026               |                                   **A$28.9M median modeled cost** | Doing nothing leaves substantial expected exposure                                    |
| C+D+E decision scenario       | **A$28.0M median modeled cost; 61.49% probability of lower cost** | Pilot the portfolio, but do not describe the modeled difference as guaranteed savings |
| Hiring efficiency             |         **Agency fees are approximately 4× the Direct benchmark** | Test Direct sourcing as a separate operational cost lever                             |

The overall management logic is:

> **Keep valuable people → avoid expensive replacement → hire more efficiently.**

---

## What problem did the analysis solve?

### 1. Not every recorded voluntary exit is a retention problem

NovaCorp recorded 1,133 voluntary exits during the analysis window. However, 688—or approximately 61%—were classified as employer-initiated `push` exits.

The relevant retention population is therefore defined as:

```text
Voluntary exit
AND employee-initiated pull pathway
AND Outstanding, High Performer, or HiPo
```

This produces **341 genuine regrettable exits over 24 months**.

Using the case replacement-cost convention:

```text
Replacement exposure
= salary at exit × 1.5 × 85% backfill
```

these exits represent approximately **A$27.5M in annual replacement exposure**.

This A$27.5M is the central retention problem used throughout the dashboard.

### 2. The broader workforce-cost total requires an evidence boundary

Finance reported approximately A$42M in annual people-cost leakage. Reconstructing the three supplied cost buckets gives approximately A$45.9M:

* A$27.5M genuine regrettable attrition;
* A$13.1M disengagement productivity exposure; and
* A$5.25M hiring inefficiency.

These buckets do not have equal evidential strength.

The A$13.1M disengagement figure reproduces the case’s 15% productivity-loss assumption. The observed goal-achievement gap supports only approximately A$0.53M and is statistically inconclusive.

The dashboard therefore treats **A$27.5M as the strongly reconciled retention problem**, while showing the wider estimate with a clear assumption boundary.

---

## How the analytical story was built

The dashboard follows the same reasoning chain as the finalized analysis.

| Stage                | Business question                                     | Analytical conclusion                                                                        | Dashboard location                 |
| -------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Problem**          | What is NovaCorp actually losing?                     | 341 genuine regrettable exits create A$27.5M/year of replacement exposure                    | Decision overview                  |
| **Measurement**      | Can HR currently see the target population?           | The existing flag detects only 34.6% and misses A$17.8M/year                                 | Decision overview and Evidence map |
| **Warning boundary** | Can engagement identify likely leavers?               | No reliable individual-level warning was validated                                           | Decision overview and Evidence map |
| **Drivers**          | Where is there a plausible mechanism for action?      | HiPo career friction, integration timing, and senior R&C pressure                            | Driver cards                       |
| **Economics**        | Which interventions can plausibly pay for themselves? | C, D, and E survive the decision filters; A and B fail break-even arithmetic                 | Strategy simulator                 |
| **Scenario**         | What might happen if NovaCorp acts?                   | The model compares status quo with individual and combined interventions under uncertainty   | Strategy simulator                 |
| **Test**             | What evidence would justify scaling?                  | Future observed outcomes, financial value, delivery and fairness must pass predeclared gates | Pilot scorecard                    |
| **Governance**       | What must the analysis never become?                  | No employee risk labels, manager rankings, causal overclaims, or small-cell disclosure       | Governance                         |

This structure keeps five different ideas separate:

> **Finding → Evidence → Boundary → Action → Test**

---

## Why HR’s current measurement is insufficient

The current regrettable-exit flag identifies:

* **118 true positives**;
* **223 false negatives**; and
* **35 false positives**.

This gives:

* **34.6% recall**: HR sees only about one-third of the genuine target exits;
* **77.1% precision**: most flagged exits are relevant, but many relevant exits are never flagged;
* **A$9.7M/year visible exposure**; and
* **A$17.8M/year missed exposure**.

The first recommendation is therefore not a predictive model. It is a corrected three-field measurement rule and reconciliation process.

The dashboard uses the finalized definition consistently. It does not attempt to assign individual employees a probability of resignation.

---

## Why the dashboard does not use engagement as a flight-risk score

The finalized analysis found that genuine regrettable leavers were still engaged and responsive before departure:

* approximately **84%** responded to their final pre-exit survey;
* their final engagement score was only **0.12 standard deviations below average**;
* the difference from stayers was not statistically conclusive; and
* there was no meaningful within-person engagement deterioration.

The observable disengagement signature mainly belonged to `push` exits, not the high-value `pull` exits NovaCorp is trying to retain.

Therefore:

* engagement may support confidential and voluntary outreach;
* missing responses should not be ignored;
* but engagement must not be used for employee risk rankings, “likely leaver” labels, promotion decisions, discipline, or retention-budget allocation.

This is why the dashboard models **cohort conditions**, not individual employee behavior.

---

## The three structural drivers

### C — HiPo career friction

HiPos experienced:

* **3.84 exits per 100 person-years**, compared with 1.14 among other employees;
* **rate ratio 3.36**;
* **95% confidence interval 2.60–4.36**; and
* approximately **A$8.7M in historical annual exposure**.

This is the strongest structural cohort finding.

However, the evidence does not show that every HiPo is about to leave or that HiPo status causes attrition. It supports prioritizing a valuable cohort for structured career management.

### D — Integration shock on a schedule

Entity B and Entity C exits were associated with integration milestones rather than a permanently elevated background rate.

The analysis therefore models integration risk as:

```text
steady-state baseline + a dated consolidation pulse
```

The finalized 2026 scenario assumes approximately:

* **16.1 incremental exits**; and
* **A$2.46M of reachable pulse exposure**.

This creates a time-sensitive intervention opportunity before the relevant milestone.

### E — Senior Risk & Compliance pressure

Senior Risk & Compliance combines:

* approximately **4.2 exits per 100 person-years**;
* five consecutive below-firm survey waves for confidence in role future; and
* approximately **A$5.9M in historical annual exposure**.

The senior-rate result rests on only five exits. The recommendation is therefore supported by triangulation across attrition, survey evidence, regulatory context, and the Annual Report—not by sample size alone.

### Why the three historical exposure figures are not added

The historical C, D, and E cohorts overlap. For example, a HiPo in Entity B and Risk & Compliance could appear in all three driver views.

After de-duplication:

* **193 exits** fall within at least one named driver;
* these exits represent approximately **A$15.8M/year**;
* this is approximately **57% of the A$27.5M problem**; and
* the remaining **148 exits and A$11.7M/year** have no shared observed mechanism.

The dashboard deliberately does not recommend a generic intervention for the residual A$11.7M. Funding a programme without a mechanism would be spending without a testable thesis.

---

## Why C, D, and E enter the simulator

C, D, and E are not the only workforce factors NovaCorp considered.

They are the three retention interventions that survived the finalized decision filters:

1. an observable structural problem exists;
2. the mechanism is plausible;
3. a specific owner can act;
4. the addressable exposure can be estimated;
5. the programme has a finite cost;
6. break-even efficacy is below 100%;
7. the action can be tested in a bounded pilot; and
8. the action does not require employee-level prediction.

| Option | Intervention                       | Annual cost |              2026 addressable exposure | Break-even efficacy | Decision             |
| ------ | ---------------------------------- | ----------: | -------------------------------------: | ------------------: | -------------------- |
| **A**  | Blanket HiPo pay adjustment        |    A$13.10M |                                A$9.01M |              145.3% | Reject               |
| **B**  | Promote all eligible HiPos         |    A$14.47M | Only about 27% of A$9.01M is reachable |              602.1% | Reject               |
| **C**  | HiPo career programme              |     A$1.75M |                                A$9.01M |               19.5% | Pilot                |
| **D**  | Entity B milestone playbook        |     A$1.00M |                                A$2.46M |               40.6% | Time-sensitive pilot |
| **E**  | R&C FAR readiness and role clarity |     A$0.60M |                                A$2.69M |               22.3% | Pilot                |

Options A and B are rejected by arithmetic, not preference. Their costs exceed the exposure they can credibly address.

This also explains why the surviving interventions are process-led rather than blanket salary-led.

---

## What each surviving strategy actually means

### C — HiPo career programme

Owner: **Talent & Reward**

The programme includes:

* documented progression criteria;
* structured career conversations;
* explicit reassessment dates;
* internal-mobility and development options; and
* a funded pool of 20 accelerated promotions per year.

This is not automatic promotion for every HiPo.

### D — Entity B milestone playbook

Owner: **Integration Programme**

The programme includes:

* milestone communications;
* role and organizational clarity;
* targeted retention conversations; and
* implementation before the predicted consolidation pulse.

It applies the logic of the Entity A integration precedent to a dated Entity B risk.

### E — R&C FAR programme

Owner: **CRO with HR**

The programme includes:

* FAR-readiness support;
* accountability and role-clarity work;
* confidence-in-role-future monitoring; and
* market benchmarking before considering broader compensation action.

The A$0.60M model values replacement exposure only. It does not price wider regulatory or operational risk.

---

## How to use the dashboard

## 1. Decision overview

Start here to understand the case in executive order.

Look for:

1. **A$27.5M genuine regrettable-attrition exposure**
   This establishes the size of the strongly supported retention problem.

2. **A$17.8M currently invisible to HR**
   This explains why NovaCorp must fix measurement before relying on more advanced analytics.

3. **A$15.8M inside three bounded drivers**
   This shows how the analysis moves from a broad cost problem to specific, owner-led interventions.

Then follow the three driver cards from left to right:

```text
Career progression → integration timing → R&C role pressure
```

Each card separates:

* historical exposure;
* 2026 reachable exposure;
* programme cost;
* break-even efficacy;
* proposed action; and
* evidence boundary.

Historical exposure and 2026 addressable exposure are related but are not interchangeable.

---

## 2. Strategy simulator

The Strategy Simulator answers:

> **What could happen if NovaCorp applies one intervention, several interventions, or no intervention at all?**

### Step 1 — Select the moves

Toggle C, D, and E on or off.

You can examine:

* one intervention independently;
* any pair of interventions;
* all three interventions together; or
* the status quo with no intervention.

This makes it possible to see whether a portfolio result is driven by one strong move or genuinely improved by combining programmes.

### Step 2 — Choose an efficacy assumption

Efficacy means:

> **The percentage of exits reachable by the selected programme that the intervention prevents.**

It does not mean a NovaCorp-wide attrition reduction.

The finalized notebook uses a Beta(3.5, 8) efficacy prior:

* mean approximately **30.4%**;
* deliberately modest;
* uncertainty concentrated roughly between 15% and 48%.

When a user changes efficacy, programme costs, or the integration pulse, the dashboard labels the result as a **derived scenario output**.

### Step 3 — Compare action with doing nothing

The two large comparison panels show:

```text
Do nothing → Take action
```

Read the output in this order:

1. median modeled annual cost;
2. difference from status quo;
3. 90% uncertainty range;
4. expected avoided exits;
5. gross replacement exposure avoided;
6. programme spend;
7. expected net value;
8. portfolio break-even efficacy; and
9. modeled probability that total cost is lower.

A lower median is encouraging, but it should never be read without the uncertainty range and probability.

### Step 4 — Examine marginal contributions

The contribution table shows what each move adds at the selected efficacy:

* expected avoided exits;
* gross exposure addressed;
* programme cost;
* expected net value; and
* break-even threshold.

This helps management identify when an intervention strengthens the portfolio and when it adds cost without enough modeled benefit.

### Step 5 — Compare all eight combinations

The comparison chart places every C/D/E combination on the same cost scale.

The dot represents the median. The horizontal line represents the 90% modeled range. The highlighted result is the currently selected strategy.

Pairwise combinations are derived from finalized segment baselines. They were not all printed as standalone notebook outputs and should therefore be described as planning scenarios.

---

## How to interpret the default scenario

Under the finalized assumptions:

| Scenario   | Median 2026 cost | Difference from status quo | Probability cost is lower |
| ---------- | ---------------: | -------------------------: | ------------------------: |
| Status quo |         A$28.91M |                          — |                         — |
| C only     |         A$27.98M |              A$0.93M lower |                    62.32% |
| D only     |         A$29.19M |             A$0.28M higher |                    45.89% |
| E only     |         A$28.69M |              A$0.21M lower |                    52.42% |
| C+D+E      |         A$28.01M |              A$0.90M lower |                    61.49% |

The correct interpretation is:

* **C is the financial anchor** of the portfolio under the default assumptions.
* **E is modestly favorable**, but uncertainty remains substantial.
* **D is below break-even as a standalone intervention at the default efficacy.**
* **C+D+E still beats status quo in the median**, but it is not clearly financially superior to C alone.
* D remains strategically relevant because it has a dated target, an internal precedent, and an observable event window.
* If management prioritizes near-term financial evidence only, it can begin with C, consider E, and hold D until the milestone design and efficacy expectation are agreed.
* If management prioritizes protection against the predicted integration event, D can remain a bounded A$1M pilot with explicit stopping rules.

The dashboard is designed to make this trade-off visible rather than force every selected intervention to appear beneficial.

---

## What happens if NovaCorp acts?

At the default C+D+E setting:

* status quo median cost is approximately **A$28.9M**;
* the portfolio median is approximately **A$28.0M**;
* the modeled difference is approximately **A$0.9M lower**; and
* the modeled probability of lower total cost is **61.49%**.

This is evidence that the portfolio is worth testing.

It is not evidence that NovaCorp is guaranteed to save A$0.9M. Programme costs are certain, while the benefit arrives through exits that may or may not be prevented.

The dashboard therefore converts the scenario into a pilot decision:

> **Test the interventions because the upside is material and measurable—not because the simulation has proven their causal effect.**

---

## Why the simulator validates a pilot rather than promising savings

The scenario model projects cohort-level outcomes, not individual resignations.

Its logic is:

```text
Status-quo cohort exit intensity
× intervention coverage
× uncertain efficacy
× replacement-cost severity
− programme cost
```

The finalized analysis first back-tested whether cohort rates could support projection:

* 2025 predicted total: approximately 201 exits;
* 2025 observed total: 174 exits;
* HiPo predicted: approximately 57 versus 52 observed;
* R&C predicted: approximately 14 versus 16 observed;
* base predicted: approximately 76 versus 69 observed;
* Entity B/C predicted: approximately 53 versus 37 observed.

The Entity B/C miss is analytically important: integration shocks should not be treated as permanent background rates. This is why D uses an explicit event pulse instead.

The simulator uses 10,000 Monte Carlo runs to represent uncertainty in:

* exit counts;
* programme efficacy; and
* total annual financial outcomes.

It therefore shows a distribution—not a savings forecast.

---

## 3. Evidence & controls

Use this page when a judge or executive asks:

* Where did this claim come from?
* What is observed versus assumed?
* What does the result not prove?
* How should NovaCorp test the recommendation?
* What employee-data uses are prohibited?

### Evidence map

Each finding is presented as:

```text
Evidence → supported decision → boundary
```

This prevents an observational association from silently becoming a causal claim.

### Assumptions

The dashboard separates four evidence layers:

| Layer                    | Meaning                                                       |
| ------------------------ | ------------------------------------------------------------- |
| **Locked evidence**      | Historical quantities reconciled to the finalized analysis    |
| **Notebook assumptions** | Finalized planning assumptions used in the reference scenario |
| **Derived scenario**     | A user-created result after changing an input                 |
| **Future observed**      | Outcomes NovaCorp must collect during a pilot                 |

### Pilot scorecard

Scale decisions should use future observed evidence, including:

* 365-day genuine regrettable pull-exit rate;
* career-conversation and progression-plan completion;
* promotion and internal-mobility outcomes;
* integration-pulse exits around the predeclared event window;
* FAR-readiness delivery and confidence-in-role-future trends;
* programme participation and implementation cost;
* avoided replacement exposure;
* realized net value against a comparison group; and
* fairness across sufficiently large employee subgroups.

### Governance

The dashboard must never be used for:

* employee flight-risk rankings;
* “likely leaver” labels;
* promotion or disciplinary decisions;
* manager performance league tables;
* publishing cells below ten;
* claiming that departments or managers caused attrition;
* treating addressable exposure as guaranteed savings; or
* claiming causal programme efficacy before a controlled evaluation.

---

## The decisions outside the C/D/E simulator

Some recommendations matter but do not belong inside the retention-effect simulation.

### Correct the exit measurement rule

This improves visibility from 34.6% recall toward complete rule-based detection by construction. It does not itself prevent exits.

### Repair exit-record data quality

`performance_band_at_exit` must reconcile with actual review history before future predictive work can be trusted.

### Run the senior HiPo Radar

NovaCorp has:

* **1,029 active HiPos**; and
* **119 active HiPos at Level 3 or above**.

The senior group should be reviewed quarterly as a value-based operating list.

The Radar answers:

> **Who would be financially important to lose, weighted by the one cohort differential the analysis validated?**

It does not answer:

> **Who is about to resign?**

Named employee-level data should remain inside NovaCorp’s controlled HR environment and must not appear in the public dashboard.

### Re-base disengagement exposure

The 15% productivity assumption is approximately 25 times the measured goal-achievement gap. The CFO should separate the finance assumption from the observed evidence.

### Shift Agency volume toward Direct sourcing

Agency hiring is a separate replacement-efficiency lever:

* approximately **137 Agency hires per year**;
* average Agency fee approximately **A$22,161 per hire**;
* Direct benchmark **A$5,500**;
* Agency fee approximately **4×** the Direct benchmark; and
* shifting 50% of annual Agency volume addresses approximately **A$1.14M in gross premium**.

This is gross addressable premium, not guaranteed net savings. Internal sourcing cost, recruiter capacity, vacancy duration, fill rate, candidate quality, retention, and diversity must be measured before scaling.

---

## Recommended management sequence

1. **Fix measurement immediately.**
   Establish the three-field genuine-regrettable-exit view and repair performance-record reconciliation.

2. **Launch the process-led retention pilots.**
   Use C as the financial anchor, consider E as a bounded pilot, and treat D as a time-sensitive decision tied to the integration milestone.

3. **Operate the senior HiPo Radar quarterly.**
   Use it as a value-based review rhythm, not a prediction model.

4. **Test Direct sourcing separately.**
   Begin with a controlled shift and measure net operational value.

5. **Pre-register the evaluation.**
   Freeze definitions, outcomes, comparison groups, financial formulas, scale gates, kill criteria, and fairness checks.

6. **Scale only after observing results.**
   Require credible retention improvement, positive net value, adequate delivery, and acceptable fairness outcomes.

---

## What the dashboard proves—and what it does not

### Supported by the finalized evidence

* Genuine regrettable attrition is financially material.
* HR’s existing flag misses most of the target population.
* HiPo status identifies a higher-rate, financially important cohort.
* Integration-related risk is event-timed.
* Senior R&C pressure warrants a bounded pilot through triangulated evidence.
* Blanket pay and blanket promotion fail financial arithmetic.
* Agency sourcing carries a substantial premium without an obvious matched quality advantage.
* Cohort-level planning is more defensible than employee-level prediction.

### Not established

* That any observed driver causes an employee to resign.
* That every HiPo is individually at high risk.
* That engagement can rank likely leavers.
* That a department or manager caused concentrated exposure.
* That the modeled A$0.9M difference will be realized.
* That Direct sourcing is operationally equivalent before the pilot measures capacity, speed, quality, retention, and diversity.
* That a programme should scale before future observed evidence passes the agreed gates.

---

## Data provenance and privacy

The dashboard is built from the finalized `NovaCorp_Story.ipynb` and the four original source tables:

* `employees.csv`
* `attrition_log.csv`
* `performance.csv`
* `engagement.csv`

The deployed application reads only:

```text
data/final_snapshot.json
```

The public repository contains aggregate evidence only. It does not contain:

* original row-level HR tables;
* employee names;
* employee IDs;
* manager IDs;
* reviewer IDs; or
* a named Radar list.

The snapshot is fingerprinted to the finalized notebook, and the rebuild process runs reconciliation checks before replacing the public dashboard data.

---

## Run locally

### Windows

The easiest option is to double-click:

```text
start_dashboard.bat
```

### Git Bash

```bash
cd /c/path/to/Accenture_Dashboard
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### PowerShell

```powershell
cd C:\path\to\Accenture_Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

## Deploy with Streamlit Community Cloud

1. Upload the contents of this repository to GitHub.
2. Do not upload the four original CSVs or the notebook.
3. Open Streamlit Community Cloud.
4. Select this repository and the `main` branch.
5. Set the main file path to `app.py`.
6. In Advanced settings, select **Python 3.12**.
7. Deploy. No secrets are required.
8. Test the public link on desktop and mobile before sharing it.

---

## Verification

Run:

```bash
python -m unittest discover -s tests -v
```

The checks cover:

* finalized headline figures;
* authoritative notebook fingerprint;
* finalized scenario outputs;
* all eight C/D/E combinations;
* ordered uncertainty intervals; and
* absence of row-level identifier fields from the public snapshot.

---

## Thirty-second walkthrough

> Start on the Decision Overview to see the A$27.5M genuine loss, the A$17.8M currently invisible to HR, and the three bounded drivers covering A$15.8M of annual exposure. Then open the Strategy Simulator and toggle C, D, and E individually or together. The two main panels compare taking action with doing nothing, while the common-scale chart shows whether combining interventions improves the decision. Finally, use Evidence & Controls to distinguish observed evidence from assumptions and to see what NovaCorp must measure before scaling. The dashboard supports controlled pilot decisions—it does not predict employees or promise savings.
