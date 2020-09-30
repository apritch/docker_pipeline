configfile: "config.yaml"

rule bwa_map:
	input:
		"shared_data/genome.fa",
		lambda wildcards: config["samples"][wildcards.sample]
	output:
		"shared_data/mapped_output/{sample}.sam"
	script:
		"scripts/bwa_map.py"
