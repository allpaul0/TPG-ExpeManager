import matplotlib.pyplot as plt
import pandas as pd

def plot_results(variable, operation, plot):
    # Read the results from CSV file
    results = pd.read_csv('results.csv')

    # Group by instrType, instrSetName and seed, apply operation to data
    if(operation == 'max'):
        grouped = results.groupby(['instrType', 'instrSetName', 'seed'])[variable].max().reset_index()
    elif(operation == 'min'):
        grouped = results.groupby(['instrType', 'instrSetName', 'seed'])[variable].min().reset_index()
    else:
        raise ValueError("Operation must be either 'max' or 'min'")
        
    # Prepare data for boxplot: one box per (instrType, scaleFactor)
    boxplot_data = []
    labels = []
    for (instrSetName, instrType), group in grouped.groupby(['instrSetName', 'instrType']):
        boxplot_data.append(group[variable])
        labels.append(f"{instrType}\n{instrSetName}")

    plt.figure(figsize=(10, 6))
    yshift = 0
    if(plot == 'boxplot'):
        plt.boxplot(boxplot_data)
        yshift = 1
    elif(plot == 'plot'):
        plt.plot(boxplot_data, 'o')
        plt.legend(set(grouped['seed'].tolist()), title='seed')
    else:
        raise ValueError("Plot must be either 'boxplot' or 'plot'")
    plt.ylabel(variable)
    plt.title(operation + ' ' + variable + ' by instrType and instrSetName (averaged by seed)')
    plt.xticks([y + yshift for y in range(len(boxplot_data))], rotation=45, labels=labels)
    plt.tight_layout()
    plt.savefig(variable + '_' + plot + '.pdf')  # Save to PDF
    plt.show()

plot_results('vSuccess', 'max', 'boxplot')
plot_results('vDistMax', 'min', 'boxplot')
plot_results('vSuccess', 'max', 'plot')
plot_results('vDistMax', 'min', 'plot')
