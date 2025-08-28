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
    elif(plot == 'eventplot'):
        plt.eventplot(boxplot_data, orientation="vertical")
    else:
        raise ValueError("Plot must be either 'boxplot' or 'eventplot'")
    plt.ylabel(variable)
    plt.title(operation + ' ' + variable + ' by instrType and instrSetName (averaged by seed)')
    plt.xticks([y + yshift for y in range(len(boxplot_data))], rotation=45, labels=labels)
    plt.tight_layout()
    plt.savefig(variable + '_' + plot + '.pdf')  # Save to PDF
    plt.show()

def plot_results_per_gen(variable):
    # Read the results from CSV file
    results = pd.read_csv('results.csv')
    
    # Group by instrType, instrSetName, and generation, then calculate mean and quartiles
    grouped = results.groupby(['instrType', 'instrSetName', 'Gen'])[variable].agg(['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).reset_index()
    grouped.columns = ['instrType', 'instrSetName', 'generation', 'mean', 'median', 'q25', 'q75']

    # For each (instrType, instrSetName), plot the mean and quartiles
    plt.figure(figsize=(12, 8))

    for (instrSetName, instrType), group in grouped.groupby(['instrSetName', 'instrType']):
        gens = group['generation'].unique()
        means = group.groupby('generation')['mean'].mean()
        q25s = group.groupby('generation')['q25'].mean()
        q75s = group.groupby('generation')['q75'].mean()

        plt.plot(gens, means, label=f"{instrType}\n{instrSetName}")
        plt.fill_between(gens, q25s, q75s, alpha=0.2)

    plt.xlabel('Generation')
    plt.ylabel('Average ' + variable)
    plt.title('Average ' + variable + ' per Generation with Quartiles')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(variable + '_per_gen.pdf')  # Save to PDF
    plt.show()

plot_results('vSuccess', 'max', 'boxplot')
plot_results('vDistMax', 'min', 'boxplot')
plot_results('vSuccess', 'max', 'eventplot')
plot_results('vDistMax', 'min', 'eventplot')

plot_results_per_gen('vSuccess')
