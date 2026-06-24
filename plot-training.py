import pandas as pd
import matplotlib.pyplot as plt

filename = "../tpg_nextflow/tpg_fixedpt_comp_logexp_trigo_complete/training_results/useInstrTrig-True_useInstrLogExp-True_useInstrExpensiveArithmetic-True_useInstrComparison-True_seed-0_instrType-fixedpt/outLogs/garbage.ods"

df = pd.read_csv(filename, sep=r"\s+", skiprows=1)

plt.plot(df["Gen"], df["tDistMax"])
plt.xlabel("Generation")
plt.ylabel("tDistMax")
plt.grid(True)
plt.show()