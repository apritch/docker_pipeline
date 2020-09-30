import subprocess

def sort_bam():

	"""function for sorting bam file using sam tools
	"""

	#create a shared directory between the host and docker container and pull the container id from the command line output
	process_share = subprocess.run('docker run -dit -P --name samtools -v /home/ashley/training/docker_pipeline/shared_data:/shared_data biocontainers/samtools:v1.7.0_cv4', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
	container_id = str(process_share.stdout)[0:4]

	#create output folder with rwx permissions so host can edit
	subprocess.run('docker exec ' + container_id + " /bin/sh -c 'mkdir -m 777 /shared_data/docker_bam_output'", shell=True)

	#run bwa
	bam = str(snakemake.output).split("/")[-1]
	command = "samtools sort /" + str(snakemake.input[0]) + " -o /shared_data/docker_bam_output/" + bam
	subprocess.run('docker exec ' + container_id + " /bin/sh -c '" + command + "'", shell=True)

	#kill and remove container
	subprocess.run('docker kill samtools', shell=True)
	subprocess.run('docker rm samtools', shell=True)

	#copy data to snakemake output directory and remove temporary docker directory
	subprocess.run('cp shared_data/docker_bam_output/' + bam + ' ' + str(snakemake.output), shell=True)
	subprocess.run('rm -rf shared_data/docker_bam_output', shell=True)

sort_bam()
