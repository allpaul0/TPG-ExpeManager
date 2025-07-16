import matplotlib.pyplot as plt
import pandas as pd


def plot_results(variable):
    # Read the results from CSV file
    results = pd.read_csv('results.csv')

    # Group by instrType and scaleFactor, aggregate max_vSuccess by seed (mean)
    grouped = results.groupby(['instrType', 'scaleFactor', 'seed'])[variable].mean().reset_index()

    # Prepare data for boxplot: one box per (instrType, scaleFactor)
    boxplot_data = []
    labels = []
    for (instrType, scaleFactor), group in grouped.groupby(['instrType', 'scaleFactor']):
        boxplot_data.append(group[variable])
        labels.append(f"{instrType}\nscale={scaleFactor}")

    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, labels=labels)
    plt.ylabel(variable)
    plt.title(variable + ' by instrType and scaleFactor (averaged by seed)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(variable + '_boxplot.pdf')  # Save to PDF
    plt.show()

plot_results('max_vSuccess')
plot_results('min_vDistMax')