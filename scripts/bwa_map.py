import subprocess

def map_reads():

	"""function for read mapping using bwa mem as part of Snakemake docker_pipeline
	"""

	#create a shared directory between the host and docker container and pull the container id from the command line output
	process_share = subprocess.run('docker run -dit -P --name bwa-test -v /home/ashley/training/docker_pipeline/shared_data:/shared_data biocontainers/bwa:v0.7.17_cv1', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
	container_id = str(process_share.stdout)[0:4]

	#create output folder with rwx permissions so host can edit
	subprocess.run('docker exec ' + container_id + " /bin/sh -c 'mkdir -m 777 /shared_data/docker_mapped_output'", shell=True)

	#run bwa
	sam = str(snakemake.output).split("/")[-1]
	command = "bwa mem /" + str(snakemake.input[0]) + ' /' + str(snakemake.input[1]) + " > /shared_data/docker_mapped_output/" + sam
	subprocess.run('docker exec ' + container_id + " /bin/sh -c '" + command + "'", shell=True)

	#kill and remove container
	subprocess.run('docker kill bwa-test', shell=True)
	subprocess.run('docker rm bwa-test', shell=True)

	#copy data to snakemake output directory and remove temporary docker directory
	subprocess.run('cp shared_data/docker_mapped_output/' + sam + ' ' + str(snakemake.output), shell=True)
	subprocess.run('rm -rf shared_data/docker_mapped_output', shell=True)

map_reads()
