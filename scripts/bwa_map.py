import subprocess

#create a shared directory between the host and docker container and pull the container id from the command line output
process = subprocess.run('docker run -dit -P --name bwa-test -v /home/ashley/training/docker_pipeline/data:/shared_data biocontainers/bwa:v0.7.17_cv1', shell=True, check=True, stdout=subprocess.PIPE, universal_newlines=True)
container_id = str(process.stdout)[0:4]

#create output folder with rwx permissions so host can edit
subprocess.run('docker exec ' + container_id + " /bin/sh -c 'mkdir -m 777 /shared_data/mapped_output'", shell=True)

#run bwa
subprocess.run('docker exec ' + container_id + " /bin/sh -c 'bwa mem /shared_data/genome.fa /shared_data/samples/A.fastq > /shared_data/mapped_output/A.sam'", shell=True)

#kill and remove container
subprocess.run('docker kill bwa-test', shell=True)
subprocess.run('docker rm bwa-test', shell=True)
