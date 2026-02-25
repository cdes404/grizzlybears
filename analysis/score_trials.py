#!/usr/bin/env python3
"""
score_trials.py

Reads:
  1) reVISit export CSV (raw participant responses)
  2) accurate_density_comps.csv (State 1, State 2, Population Density Difference Percentage)

Outputs:
  - master_scored.csv: one row per answered q-density trial, with truePercent, rawError, log2Error
  - summary_by_condition.csv: mean/median log2Error by visualization condition
  - summary_by_trial.csv: mean/median log2Error by trial pair
"""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import pandas as pd


# --- Helpers ---------------------------------------------------------------

STATE_NORMALIZE = {
    # trialId-style concatenations -> proper names
    "Uttarpradesh": "Uttar Pradesh",
    "Westbengal": "West Bengal",
    "Tamilnadu": "Tamil Nadu",
    "Andhrapradesh": "Andhra Pradesh",
    "Himachalpradesh": "Himachal Pradesh",
    "Madhyapradesh": "Madhya Pradesh",
    "JammuandKashmir": "Jammu and Kashmir",
    # add more if you introduce new pairs later
}

def clean_state_name(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip()

    # If it's already spaced properly, keep it
    if s in STATE_NORMALIZE.values():
        return s

    # Normalize weird spacing/case
    # Remove extra spaces
    s = re.sub(r"\s+", " ", s)

    # Try exact normalize mapping for concatenated names
    if s in STATE_NORMALIZE:
        return STATE_NORMALIZE[s]

    return s

def normalize_key(a: str, b: str) -> tuple[str, str]:
    """Key for lookup dictionary, exact order matters (A compared to B)."""
    return (clean_state_name(a), clean_state_name(b))

def parse_condition(trial_id: str) -> str:
    """
    trialId examples:
      Delhi-Bihar-RGB
      Uttarakhand-Himachalpradesh-G
      Rajasthan-Haryana-R
    Return: 'RGB' or 'R' or 'G' or 'UNKNOWN'
    """
    if not isinstance(trial_id, str):
        return "UNKNOWN"
    parts = trial_id.split("-")
    if len(parts) < 3:
        return "UNKNOWN"
    cond = parts[-1].strip()
    if cond in {"R", "G", "RGB"}:
        return cond
    return "UNKNOWN"

def parse_states_from_prompt(prompt: str) -> tuple[str, str] | None:
    """
    Prompt example:
      "How much more dense is the population in Delhi compared to Bihar?"
    Return: ("Delhi", "Bihar") = (State 1, State 2)
    """
    if not isinstance(prompt, str):
        return None

    # grab: "in X compared to Y"
    m = re.search(r"in\s+(.+?)\s+compared\s+to\s+(.+?)(?:\?|$)", prompt, flags=re.IGNORECASE)
    if not m:
        return None

    a = m.group(1).strip()
    b = m.group(2).strip()

    # remove any trailing punctuation/newlines
    a = re.sub(r"[\n\r]+", " ", a).strip()
    b = re.sub(r"[\n\r]+", " ", b).strip()

    return (clean_state_name(a), clean_state_name(b))

def parse_states_from_trial_id(trial_id: str) -> tuple[str, str] | None:
    """
    trialId example: Uttarakhand-Himachalpradesh-G
    Return: ("Uttarakhand", "Himachal Pradesh")
    NOTE: This order might not match prompt wording (your prompt might flip it),
          so we prefer the prompt when available.
    """
    if not isinstance(trial_id, str):
        return None
    parts = trial_id.split("-")
    if len(parts) < 3:
        return None
    a_raw, b_raw = parts[0], parts[1]
    return (clean_state_name(a_raw), clean_state_name(b_raw))

def compute_log2_error(raw_error: float) -> float:
    """
    Cleveland & McGill-style scaling (per your assignment note):
      log2Error = log2(rawError + 0.125)
    With the special case:
      if rawError == 0, log2Error = 0
    """
    if raw_error == 0:
        return 0.0
    return math.log2(raw_error + 0.125)


# --- Main ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Score reVISit density comparison trials.")
    parser.add_argument("--raw", required=True, help="Path to reVISit export CSV (raw).")
    parser.add_argument("--lookup", required=True, help="Path to accurate_density_comps.csv.")
    parser.add_argument("--out", default="data/processed/master_scored.csv", help="Output scored CSV.")
    parser.add_argument("--summary_condition", default="data/processed/summary_by_condition.csv",
                        help="Output summary CSV by condition.")
    parser.add_argument("--summary_trial", default="data/processed/summary_by_trial.csv",
                        help="Output summary CSV by trial pair.")
    args = parser.parse_args()

    raw_path = Path(args.raw)
    lookup_path = Path(args.lookup)
    out_path = Path(args.out)
    sum_cond_path = Path(args.summary_condition)
    sum_trial_path = Path(args.summary_trial)

    # Ensure output dirs exist
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sum_cond_path.parent.mkdir(parents=True, exist_ok=True)
    sum_trial_path.parent.mkdir(parents=True, exist_ok=True)

    # Read input files
    raw = pd.read_csv(raw_path)
    lookup = pd.read_csv(lookup_path)

    # Standardize lookup columns (strip spaces)
    lookup.columns = [c.strip() for c in lookup.columns]

    # Expect these columns from your lookup:
    # "State 1", " State 2", " Population Density Difference Percentage " (your pasted version has spaces)
    # We'll handle flexible naming by stripping.
    # Find best column matches:
    def find_col(df: pd.DataFrame, target: str) -> str:
        target_low = target.lower()
        for c in df.columns:
            if c.lower() == target_low:
                return c
        raise ValueError(f"Could not find column '{target}' in {list(df.columns)}")

    col_state1 = find_col(lookup, "State 1")
    col_state2 = find_col(lookup, "State 2")
    col_true = find_col(lookup, "Population Density Difference Percentage")

    # Build lookup dict: (state1, state2) -> truePercent
    true_map: dict[tuple[str, str], int] = {}
    for _, r in lookup.iterrows():
        a = clean_state_name(r[col_state1])
        b = clean_state_name(r[col_state2])
        v = r[col_true]
        if pd.isna(v):
            continue
        true_map[(a, b)] = int(round(float(v)))

    # Filter rows: keep only q-density responses with numeric answers
    raw["responseId"] = raw.get("responseId", "").astype(str)
    is_density = raw["responseId"].str.startswith("q-density")

    # Answer column name is "answer" in your export
    if "answer" not in raw.columns:
        raise ValueError("Expected column 'answer' in raw export.")

    # Clean answers: keep only numeric values
    raw["answer_num"] = pd.to_numeric(raw["answer"], errors="coerce")
    has_answer = raw["answer_num"].notna()

    df = raw[is_density & has_answer].copy()

    # Add condition
    df["condition"] = df["trialId"].apply(parse_condition)

    # Parse state order: prefer prompt order (because your prompt sometimes flips the pair)
    df["state1"] = ""
    df["state2"] = ""

    for idx, row in df.iterrows():
        prompt = row.get("responsePrompt", None)
        trial_id = row.get("trialId", None)

        parsed = parse_states_from_prompt(prompt)
        if parsed is None:
            parsed = parse_states_from_trial_id(trial_id)

        if parsed is None:
            df.at[idx, "state1"] = ""
            df.at[idx, "state2"] = ""
        else:
            df.at[idx, "state1"] = parsed[0]
            df.at[idx, "state2"] = parsed[1]

    # Lookup truePercent using (state1 compared to state2)
    def lookup_true(row) -> float:
        key = normalize_key(row["state1"], row["state2"])
        return true_map.get(key, float("nan"))

    df["truePercent"] = df.apply(lookup_true, axis=1)

    # Drop rows we cannot score (missing truePercent)
    before = len(df)
    df = df[df["truePercent"].notna()].copy()
    after = len(df)

    # Compute errors
    df["reportedPercent"] = df["answer_num"].round(0).astype(int)
    df["truePercent"] = df["truePercent"].round(0).astype(int)
    df["rawError"] = (df["reportedPercent"] - df["truePercent"]).abs()
    df["log2Error"] = df["rawError"].apply(lambda x: 0.0 if x == 0 else compute_log2_error(float(x)))

    # Add a helpful "trialPair" label
    df["trialPair"] = df["state1"].astype(str) + " vs " + df["state2"].astype(str)

    # Keep a clean set of columns for export
    keep_cols = [
        "participantId",
        "trialId",
        "trialOrder",
        "condition",
        "responseId",
        "state1",
        "state2",
        "truePercent",
        "reportedPercent",
        "rawError",
        "log2Error",
        "trialPair",
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]
    scored = df[keep_cols].sort_values(["participantId", "trialOrder"])

    scored.to_csv(out_path, index=False)

    # Summaries
    summary_by_condition = (
        scored.groupby("condition", dropna=False)
        .agg(
            n_trials=("log2Error", "count"),
            mean_log2Error=("log2Error", "mean"),
            median_log2Error=("log2Error", "median"),
            mean_rawError=("rawError", "mean"),
        )
        .reset_index()
        .sort_values("mean_log2Error")
    )
    summary_by_condition.to_csv(sum_cond_path, index=False)

    summary_by_trial = (
        scored.groupby(["trialPair", "condition"], dropna=False)
        .agg(
            n_trials=("log2Error", "count"),
            mean_log2Error=("log2Error", "mean"),
            median_log2Error=("log2Error", "median"),
            mean_rawError=("rawError", "mean"),
        )
        .reset_index()
        .sort_values(["condition", "mean_log2Error"])
    )
    summary_by_trial.to_csv(sum_trial_path, index=False)

    print("✅ Done.")
    print(f"Raw density rows before scoring: {before}")
    print(f"Scored rows after dropping missing truePercent: {after}")
    print(f"Scored CSV: {out_path}")
    print(f"Summary by condition: {sum_cond_path}")
    print(f"Summary by trial: {sum_trial_path}")

    # If rows were dropped, warn user (usually means mismatch in state naming/prompt parsing)
    dropped = before - after
    if dropped > 0:
        print(f"⚠️  Dropped {dropped} rows because no truePercent match was found.")
        print("   This usually means a mismatch between prompt state names and your lookup CSV.")
        print("   If needed, we can add more STATE_NORMALIZE entries or tweak the prompt regex.")


if __name__ == "__main__":
    main()