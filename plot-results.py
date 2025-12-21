import matplotlib.pyplot as plt
import pandas as pd

def plot_results(csv_file, variable):
    results = pd.read_csv(csv_file)

    # Keep only Gen == 99
    gen99 = results[results['Gen'] == 99]

    # One value per (instrType, instrSetName, seed)
    grouped = gen99.groupby(
        ['instrType', 'instrSetName', 'seed'],
        as_index=False
    )[variable].mean()

    # ---- ORDER DEFINITIONS ----
    instrType_order = ['double', 'float', 'fixedpt']

    instrSet_order = [
        'comp',
        'logexp',
        'trigo',
        'complete',
        'l2e2_compBare',
        'l2e2_compZmmul',
        'l2e2_compExpAr'
    ]

    # ---- EXACT LABELS (AS DEFINED) ----
    instrSet_labels = {
        'comp': "*,/,>,-,+",
        'logexp': "log,exp," + "*,/,>,-,+",
        'trigo': "trig," + "*,/,>,-,+",
        'complete': "trig," + "log,exp," + "*,/,>,-,+",
        'l2e2_compBare': "log2,exp2," + ">,-,+",
        'l2e2_compZmmul': "log2,exp2," + "*" + ">,-,+",
        'l2e2_compExpAr': "log2,exp2," + "*,/" + ">,-,+"
    }

    # ---- COLOR PER instrType ----
    instrType_colors = {
        'double': '#FFA123',   # orange
        'float': '#FFF600',    # yellow
        'fixedpt': '#18DCDC'   # light blue
    }

    # ---- PREPARE BOXPLOT DATA IN ORDER ----
    boxplot_data = []
    labels = []
    box_instrTypes = []

    for instrType in instrType_order:
        for instrSet in instrSet_order:
            subset = grouped[
                (grouped['instrType'] == instrType) &
                (grouped['instrSetName'] == instrSet)
            ]

            if not subset.empty:
                boxplot_data.append(subset[variable])
                labels.append("{" + instrSet_labels[instrSet] + "} " + instrType)
                box_instrTypes.append(instrType)

    # ---- PLOT ----
    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(
        boxplot_data,
        showmeans=False,
        patch_artist=True
    )

    # Apply colors
    for box, instrType in zip(bp['boxes'], box_instrTypes):
        box.set_facecolor(instrType_colors[instrType])

    plt.ylabel(variable)
    plt.title('Accuracy by dType and iSet')
    plt.xticks(range(1, len(labels) + 1),labels,rotation=45,ha='right')
    plt.tight_layout()
    plt.savefig(f"{variable}_boxplot.pdf")
    plt.show()


csv_file = 'results_fixedpt_float_double.csv'
plot_results(csv_file, 'vDistMax')
# plot_results(csv_file, 'vSuccess')
