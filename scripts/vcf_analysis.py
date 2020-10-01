import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pysam import VariantFile
import statistics

#save quality scores from vcf as a list
quals = [record.qual for record in VariantFile(snakemake.input[0])]

#calculate mean quality score
mean = statistics.mean(quals)

#variant count
count = len(quals)

#count of variants that passed filtering
passed = 0
for record in VariantFile(snakemake.input[0]):
	if 'pass' in record.filter:
		passed += 1

#plot and save qaulity
plt.hist(quals)
plt.savefig(snakemake.output[0])

#write basic summary file
sample = str(snakemake.input[0]).split('/')[-1]
with open(snakemake.output[1], 'w') as f:
	f.write("Sample " + sample + " recorded " + str(count) + " variants.\n")
	f.write(str(passed) + " variants passed filtering.\n")
	f.write("The mean quality score was " + str(mean) + ".")
