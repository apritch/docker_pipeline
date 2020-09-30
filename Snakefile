configfile: "config.yaml"

rule bwa_map:
	input:
		"shared_data/genome.fa",
		lambda wildcards: config["samples"][wildcards.sample]
	output:
		"shared_data/mapped_output/{sample}.sam"
	script:
		"scripts/bwa_map.py"

rule sam_bam_conversion:
	input:
		"shared_data/mapped_output/{sample}.sam"
	output:
		"shared_data/bam_output/{sample}.bam"
	script:
		"scripts/sam_bam_conversion.py"
