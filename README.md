# NovaCorp Decision Lab

A standalone Streamlit decision dashboard built from the finalized `NovaCorp_Story.ipynb` and the four original source tables. The running app reads only `data/final_snapshot.json`, so it does **not** require Gia's, Nick's, or any other teammate's processed files.

The public package contains aggregate evidence only. It includes no employee names, employee IDs, manager IDs, reviewer IDs, or original row-level HR tables.

## Start on Windows

The easiest method is to double-click `start_dashboard.bat`. It creates a local environment, installs the required packages, and opens the dashboard.

For Git Bash, run:

```bash
cd /c/path/to/NovaCorp_Decision_Dashboard
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

For PowerShell, run:

```powershell
cd C:\path\to\NovaCorp_Decision_Dashboard
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If PowerShell blocks activation, skip activation and use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## How to use the dashboard

### 1. Decision overview

Read this page as a short executive story:

1. The true target is 341 genuine regrettable exits and A$27.5M annual replacement exposure.
2. The current HR flag finds only 34.6%; 223 exits and A$17.8M/year were missed.
3. Engagement does not provide a reliable employee-level warning.
4. Three bounded mechanisms—HiPo progression, integration timing, and R&C role uncertainty—support three testable pilot moves.

### 2. Strategy simulator

Use this page in order from top to bottom:

1. Switch C, D, or E on and off. You can test one move or any combination.
2. Select an efficacy assumption. This means the percentage of *reachable* exits prevented—not a NovaCorp-wide attrition reduction.
3. Compare `Do nothing` with the selected strategy immediately.
4. Read expected avoided exits, gross exposure avoided, programme spend, expected net value, portfolio break-even, and probability that total cost is lower.
5. Use the all-combination chart to compare all eight choices on the same cost scale.

The default C+D+E view reproduces the finalized notebook's Monte Carlo output: A$28.0M median 2026 cost versus A$28.9M under status quo, with a 61.49% modeled probability of lower total cost. This supports a controlled pilot, not a guaranteed-savings claim.

The dashboard labels two result types:

- **Final notebook output:** a value printed by the finalized analysis under its locked assumptions.
- **Derived scenario output:** a planning result created after changing a control or using a combination not printed separately in the notebook.

Options A and B are shown but rejected because their break-even efficacy exceeds 100%. Measurement reform, the senior HiPo Radar, and Direct sourcing still matter, but they are kept outside the C/D/E retention simulation because they answer different decisions.

### 3. Evidence & controls

Use the four compact tabs to answer judge or client questions:

- `Evidence map`: observation, supported decision, and analytical boundary.
- `Assumptions`: what is locked evidence versus a planning assumption.
- `Pilot scorecard`: what NovaCorp must measure before scaling.
- `Governance`: permitted and prohibited uses of employee data.

## A simple teammate explanation

> Start on the overview to see the actual loss and why HR currently misses it. In the simulator, toggle C, D and E individually or together. The two large panels compare doing nothing with action, while the chart below puts all eight combinations on the same scale. The default is the finalized notebook scenario; changed controls are clearly marked as derived. The dashboard supports a pilot decision, not a causal claim or employee risk ranking.

## Publish with Streamlit Community Cloud

1. Create a new GitHub repository and upload the **contents of this folder**.
2. Do not add the four original CSVs or the notebook; the aggregate snapshot is already included.
3. In Streamlit Community Cloud, create an app from the repository.
4. Set the main file path to `app.py` and deploy. No secrets are required.
5. Test the public link on desktop and mobile, then share that URL with the submission.

## Optional: rebuild the aggregate snapshot

You do not need to rebuild anything to run or deploy the app. If the finalized notebook or original tables change, place the four original CSVs together and run:

```bash
python scripts/build_snapshot.py --raw-dir /path/to/original/csvs --notebook /path/to/NovaCorp_Story.ipynb
```

The builder refuses any notebook whose SHA-256 fingerprint does not match the finalized version and runs reconciliation gates before replacing the snapshot.

## Verification

Run the data-contract and scenario tests with:

```bash
python -m unittest discover -s tests -v
```

The checks cover the finalized headline figures, notebook scenario outputs, all eight C/D/E combinations, and the absence of row-level identifiers from the public snapshot.
