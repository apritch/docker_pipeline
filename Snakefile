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

rule sort_bam:
	input:
		"shared_data/bam_output/{sample}.bam"
	output:
		"shared_data/sorted_bam_output/{sample}.bam"
	script:
		"scripts/sort_bam.py"

rule index_bam:
	input:
		"shared_data/sorted_bam_output/{sample}.bam"
	output:
		"shared_data/sorted_bam_output/{sample}.bam.bai"
	shell:
		"samtools index {input}"

rule bcftools_call:
	input:
		fa = "shared_data/genome.fa",
		bam ="shared_data/sorted_bam_output/{sample}.bam",
		bai = "shared_data/sorted_bam_output/{sample}.bam.bai"
	output:
		"shared_data/vcf_output/{sample}.vcf"
	shell:
		"samtools mpileup -g -f {input.fa} {input.bam} | "
		"bcftools call -mv > {output}"

