import pandas as pd
import numpy as np

# Load scored data
df = pd.read_csv("data/processed/master_scored.csv")

results = []

n_boot = 5000

for condition, group in df.groupby("condition"):
    values = group["log2Error"].values
    means = []

    for _ in range(n_boot):
        sample = np.random.choice(values, size=len(values), replace=True)
        means.append(np.mean(sample))

    lower = np.percentile(means, 2.5)
    upper = np.percentile(means, 97.5)
    mean = np.mean(values)

    results.append({
        "condition": condition,
        "mean_log2Error": mean,
        "ci_lower": lower,
        "ci_upper": upper
    })

summary = pd.DataFrame(results).sort_values("mean_log2Error")
summary.to_csv("data/processed/summary_with_ci.csv", index=False)

print(summary)