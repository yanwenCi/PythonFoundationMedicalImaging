import numpy as np
import matplotlib.pyplot as plt 

#We calculated the mean, which is the average measurement. Clinician 1’s average was 6.35 cm, and Clinician 2’s was 5.94 cm.
#We also calculated the standard deviation, which tells us how spread out the measurements are. It was about 2.4 cm for both 
# clinicians, so their measurements had a similar amount of variation.
#To find the most common measurement range, we grouped the numbers into 1 cm bins, such as 6 to less than 7 cm. Across both 
# files, the busiest bin was 7 to less than 8 cm.

c1 = np.loadtxt("./clinician_1.txt")
c2 = np.loadtxt("./clinician_2.txt")
assert c1.shape == c2.shape

# Fixed 1 cm bins: [2, 3), [3, 4), ...
bins = np.arange(2, 16, 1)



for name, values in [("Clinician 1", c1), ("Clinician 2", c2)]:
    counts, edges = np.histogram(values, bins=bins)
    modal = np.flatnonzero(counts == counts.max())
    print(name)
    print("Mean:", np.mean(values))
    print("Sample SD:", np.std(values, ddof=1))
    print("Median:", np.median(values))
    print("Range:", np.min(values), np.max(values))
    print("Modal bins:", [(edges[i], edges[i + 1]) for i in modal])
    print("Modal bin count:", counts.max())


# Calculate paired differences
difference = c2 - c1
absolute_difference = np.abs(difference)
average = (c1 + c2) / 2
flagged = np.abs(difference) > 1



print("Mean absolute disagreement:", absolute_difference.mean())
print("Mean signed difference:", difference.mean())

flagged_mask = (absolute_difference > 1)
flagged = np.flatnonzero(flagged_mask)
print("Case, clinician 1, clinician 2, absolute disagreement:")
print(np.column_stack((
    flagged + 1, c1[flagged], c2[flagged], absolute_difference[flagged]
)))

fig = plt.figure(figsize=(10, 5))


# 1. Histogram: compare measurement distributions
bins = np.arange(
    np.floor(min(c1.min(), c2.min())),
    np.ceil(max(c1.max(), c2.max())) + 1,
    1
)

plt.hist(
    [c1, c2],
    bins=bins,
    label=["Clinician 1", "Clinician 2"],
    color=["steelblue", "orange"]
)
plt.title("Measurement distributions")
plt.xlabel("Measurement (cm)")
plt.ylabel("Number of measurements")
plt.legend()
plt.show()


fig, axes = plt.subplots(1, 3, figsize=(17, 5))


axes[0].hist(
    [c1, c2],
    bins=bins,
    label=["Clinician 1", "Clinician 2"],
    color=["steelblue", "orange"]
)
axes[0].set(
    title="Measurement distributions",
    xlabel="Measurement (cm)",
    ylabel="Number of measurements"
)
axes[0].legend()

# 2. Scatter plot: compare paired measurements
minimum = min(c1.min(), c2.min()) - 0.5
maximum = max(c1.max(), c2.max()) + 0.5

axes[1].plot(
    [minimum, maximum], [minimum, maximum],
    "k--", label="Equal measurements"
)
axes[1].scatter(
    c1[~flagged_mask], c2[~flagged_mask],
    color="steelblue", label="Difference ≤1 cm"
)
axes[1].scatter(
    c1[flagged_mask], c2[flagged_mask],
    color="crimson", label="Difference >1 cm"
)
axes[1].set(
    title="Paired measurements",
    xlabel="Clinician 1 (cm)",
    ylabel="Clinician 2 (cm)",
    xlim=(minimum, maximum),
    ylim=(minimum, maximum)
)
axes[1].set_aspect("equal", adjustable="box")
axes[1].legend()


bias = np.mean(difference)
sd_difference = np.std(difference, ddof=1)
lower_limit = bias - 1.96 * sd_difference
upper_limit = bias + 1.96 * sd_difference

# 3. Bland–Altman plot: differences against average size
axes[2].axhspan(-1, 1, color="lightgrey", alpha=0.4,
                label="Within ±1 cm")
axes[2].scatter(
    average[~flagged_mask], difference[~flagged_mask],
    color="steelblue"
)
axes[2].scatter(
    average[flagged_mask], difference[flagged_mask],
    color="crimson"
)

axes[2].axhline(
    bias, color="steelblue",
    label=f"Mean difference: {bias:.3f} cm"
)
axes[2].axhline(
    lower_limit, color="black", linestyle="--",
    label="Mean difference ±1.96 SD"
)
axes[2].axhline(upper_limit, color="black", linestyle="--")

for i in np.flatnonzero(flagged):
    axes[2].annotate(
        str(i + 1),
        (average[i], difference[i]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

axes[2].set(
    title="Bland–Altman agreement",
    xlabel="Mean of the two measurements (cm)",
    ylabel="Clinician 2 − Clinician 1 (cm)"
)
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("clinician_visualisation.png", dpi=200)
plt.show()