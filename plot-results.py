import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Mapping of instrType to display names
instrType_display = {
    'double': 'fp64',
    'float': 'fp32',
    'fixedpt': 'fix16.16'
}

def prepare_best_per_seed(csv_file, variable, normalized_values=False):
    """
    Returns a dataframe with the best result per seed, consistent for plotting and stats.
    If normalized_values is True and variable == 'vDistMax', divides distances by 300 and converts to %.
    """
    results = pd.read_csv(csv_file)

    if variable == "vSuccess":
        best_per_seed = results.groupby(['instrType', 'instrSetName', 'seed'], as_index=False)[variable].max()
        best_per_seed[variable] = best_per_seed[variable] * 100  # convert to percentage
        ylabel = "success rate (%) ↑"
    elif variable == "vDistMax":
        best_per_seed = results.groupby(['instrType', 'instrSetName', 'seed'], as_index=False)[variable].min()
        if normalized_values:
            best_per_seed[variable] = (best_per_seed[variable] / 300) * 100  # convert to percentage
            ylabel = "distance to objective (%) ↓"
        else:
            ylabel = "distance to objective (mm) ↓"
    else:
        raise ValueError("Unknown variable")
    
    return best_per_seed, ylabel


def plot_results(csv_file, variable, normalized_values=False, use_accuracy=False):
    
    grouped, ylabel = prepare_best_per_seed(csv_file, variable, normalized_values)

    # If requested, derive accuracy from distance_to_objective and use it as the plotted variable
    if use_accuracy:
        if 'vDistMax' not in grouped.columns:
            raise ValueError(
                "use_accuracy=True requires a 'vDistMax' column in the data."
            )
        grouped = grouped.copy()
        grouped['accuracy'] = 100-grouped['vDistMax']
        variable = 'accuracy'
        ylabel = 'Accuracy'

    # Append a percentage indicator to the ylabel when values are normalized
    if normalized_values:
        ylabel = f"{ylabel} (%)"

    instrType_order = ['double', 'float', 'fixedpt']
    instrSet_order = [
        'comp', 'logexp', 'trigo', 'complete',
        'l2e2_compBare', 'l2e2_compZmmul', 'l2e2_compExpAr'
    ]

    instrSet_labels = {
        'comp': "*,/,>,-,+",
        'logexp': "log,exp," + "*,/,>,-,+",
        'trigo': "trig," + "*,/,>,-,+",
        'complete': "trig," + "log,exp," + "*,/,>,-,+",
        'l2e2_compBare': "log2,exp2," + ">,-,+",
        'l2e2_compZmmul': "log2,exp2," + "*" + ">,-,+",
        'l2e2_compExpAr': "log2,exp2," + "*,/" + ">,-,+"
    }

    instrType_colors = {
        'double': '#FB5607',   # orange from iset dtype
        'float': '#FFBE0B',    # yellow from ISA
        'fixedpt': '#3A86FF'   # blue from uarch
    }

    boxplot_data = []
    labels = []
    box_instrTypes = []

    for instrType in instrType_order:
        for instrSet in instrSet_order:

            # discard double, fixedpt trigo, fixedpt logexp
            if not(
                instrType == 'double' or
                instrType == 'fixedpt' and 
                instrSet in ['l2e2_compZmmul', 'l2e2_compExpAr', 'trigo', 'logexp'] or #'trigo', 'logexp'
                instrType == 'float' and 
                instrSet in ['trigo', 'logexp']): #'trigo', 'logexp'
                subset = grouped[
                    (grouped['instrType'] == instrType) &
                    (grouped['instrSetName'] == instrSet)
                ]
                if not subset.empty:
                    boxplot_data.append(subset[variable])
                    display_type = instrType_display[instrType]
                    labels.append("{" + instrSet_labels[instrSet] + "} " + display_type )
                    box_instrTypes.append(instrType)

    plt.figure(figsize=(5, 4))
    bp = plt.boxplot(boxplot_data, showmeans=False, patch_artist=True)
    for box, instrType in zip(bp['boxes'], box_instrTypes):
        box.set_facecolor(instrType_colors[instrType])

    plt.ylabel(ylabel)
    plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha='right', fontsize=9)
    plt.tight_layout()
    savename = f"trained_tpgs_{variable}_boxplot{'_perc' if normalized_values else ''}.pdf"
    plt.savefig(savename)
    plt.show()


def print_tpg_stats(csv_file, variable, normalized_values=False):
    grouped, ylabel = prepare_best_per_seed(csv_file, variable, normalized_values)

    tpg_stats = grouped.groupby(['instrType', 'instrSetName'])[variable].agg(['mean', 'std']).reset_index()

    print(f"\nStatistics for {variable} ({ylabel}):")
    for _, row in tpg_stats.iterrows():
        instrType = instrType_display[row['instrType']]  # Use display names
        instrSet = row['instrSetName']
        if variable == "vSuccess" or (variable=="vDistMax" and normalized_values):
            mean_val = row['mean']
            std_val = row['std']
        else:
            mean_val = row['mean']
            std_val = row['std']
        print(f"{instrSet} {instrType}: mean={mean_val:.3f}, std={std_val:.3f}")
    
    # export to csv for pooling use print_display names and variable name in filename
    tpg_stats['instrType'] = tpg_stats['instrType'].map(instrType_display)
    tpg_stats.to_csv(f"tpg_stats_{variable}{'_perc' if normalized_values else ''}.csv", index=False)

def plot_success_and_distance(csv_file, normalized_values=False):
    # Prepare data for both variables
    vSuccess_data, vSuccess_ylabel = prepare_best_per_seed(csv_file, 'vSuccess')
    vDist_data, vDist_ylabel = prepare_best_per_seed(csv_file, 'vDistMax', normalized_values)

    instrType_order = ['double', 'float', 'fixedpt']
    instrSet_order = [
        'comp', 'logexp', 'trigo', 'complete',
        'l2e2_compBare', 'l2e2_compZmmul', 'l2e2_compExpAr'
    ]

    instrSet_labels = {
        'comp': "*,/,>,-,+",
        'logexp': "log,exp," + "*,/,>,-,+",
        'trigo': "trig," + "*,/,>,-,+",
        'complete': "trig," + "log,exp," + "*,/,>,-,+",
        'l2e2_compBare': "log2,exp2," + ">,-,+",
        'l2e2_compZmmul': "log2,exp2," + "*" + ">,-,+",
        'l2e2_compExpAr': "log2,exp2," + "*,/" + ">,-,+"
    }

    instrType_colors = {
        'double': '#FFA123',   # orange
        'float': '#FFF600',    # yellow
        'fixedpt': '#18DCDC'   # light blue
    }

    # Prepare boxplot data
    boxplot_data_success = []
    boxplot_data_dist = []
    labels = []
    box_instrTypes = []

    for instrType in instrType_order:
        for instrSet in instrSet_order:
            # vSuccess subset
            subset_succ = vSuccess_data[(vSuccess_data['instrType'] == instrType) &
                                        (vSuccess_data['instrSetName'] == instrSet)]
            # vDist subset
            subset_dist = vDist_data[(vDist_data['instrType'] == instrType) &
                                     (vDist_data['instrSetName'] == instrSet)]
            if not subset_succ.empty and not subset_dist.empty:
                boxplot_data_success.append(subset_succ['vSuccess'])
                boxplot_data_dist.append(subset_dist['vDistMax'])
                labels.append("{" + instrSet_labels[instrSet] + "} " + instrType_display[instrType])
                box_instrTypes.append(instrType)

    # Create figure with two stacked subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                                   gridspec_kw={'height_ratios': [1, 1.2]})

    # ---- Plot success on top (no x-axis labels) ----
    bp1 = ax1.boxplot(boxplot_data_success, patch_artist=True, showmeans=False)
    for box, instrType in zip(bp1['boxes'], box_instrTypes):
        box.set_facecolor(instrType_colors[instrType])
    ax1.set_ylabel(vSuccess_ylabel, fontsize=9)
    ax1.tick_params(axis='x', which='both', bottom=False, labelbottom=False)

    # ---- Plot distance on bottom (with x-axis labels) ----
    bp2 = ax2.boxplot(boxplot_data_dist, patch_artist=True, showmeans=False)
    for box, instrType in zip(bp2['boxes'], box_instrTypes):
        box.set_facecolor(instrType_colors[instrType])
    ax2.set_ylabel(vDist_ylabel, fontsize=9)
    ax2.set_xticks(range(1, len(labels) + 1))
    ax2.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)

    plt.tight_layout()
    savename = f"trained_tpgs_success_and_distance{'_perc' if normalized_values else ''}.pdf"
    plt.savefig(savename)
    plt.show()


def plot_pooled_means_and_stds(variable, normalized_values=False):

    # Data: (mean, std)
    # data = {
    #     'fp64': [(53.667, 14.370), (51.400, 12.140), (50.200, 13.290), (48.300, 7.499)],
    #     'fp32': [(54.300, 12.383), (50.600, 11.237), (53.400, 11.607), (49.800, 10.518)],
    #     'fixed': [(34.100, 8.543), (31.100, 9.279), (36.900, 7.680), (35.000, 7.732), 
    #             (34.300, 7.587), (31.200, 10.075), (29.300, 10.220)]
    # }
    
    # import data from csv
    data = {}
    df = pd.read_csv(f"tpg_stats_{variable}{'_perc' if normalized_values else ''}.csv")
    for _, row in df.iterrows():
        instrType = row['instrType']
        mean = row['mean']
        std = row['std']
        if instrType not in data:
            data[instrType] = []
        data[instrType].append((mean, std))
    
    print(data)

    pooled_means = {}
    pooled_stds = {}

    for group, values in data.items():
        means = np.array([m for m, s in values])
        stds = np.array([s for m, s in values])
        n = len(values)  # equal weighting
        
        # Pooled mean
        pooled_mean = np.mean(means)
        
        # Pooled variance: within + between
        pooled_var = np.mean(stds**2 + (means - pooled_mean)**2)
        pooled_std = np.sqrt(pooled_var)
        
        pooled_means[group] = pooled_mean
        pooled_stds[group] = pooled_std

    # Plot
    # reorder groups to have fp64, fp32, fixed
    groups = ['fp64', 'fp32', 'fix16.16']
    means = [pooled_means[g] for g in groups]
    stds = [pooled_stds[g] for g in groups]

    # print pooled means and stds
    print("\nPooled means and stds:")
    for g in groups:
        print(f"{g}: pooled mean={pooled_means[g]:.3f}, pooled std={pooled_stds[g]:.3f}")

    plt.figure(figsize=(8,5))
    plt.bar(groups, means, yerr=stds, capsize=8, color=['skyblue', 'lightgreen', 'salmon'])
    plt.ylabel("Mean value")
    plt.title("Pooled mean and std for each group")
    plt.show()

# Example usage:
csv_file = '../tpg_nextflow/tpg_expe/accuracy_results/results.csv'

# Plot and print distance as %
plot_results(csv_file, 'vDistMax', normalized_values=True, use_accuracy=True)
#print_tpg_stats(csv_file, 'vDistMax', normalized_values=True)

# Plot and print success rate normally
#plot_results(csv_file, 'vSuccess')
#print_tpg_stats(csv_file, 'vDistMax', normalized_values=False)

#plot_success_and_distance(csv_file, normalized_values=False)

#plot_pooled_means_and_stds('vDistMax', normalized_values=False)