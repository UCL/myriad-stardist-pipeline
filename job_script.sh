#!/bin/bash -l

# Job script to run a StarDist pipeline on a GPU node on Myriad

# Request 2 hours of wallclock time (format hours:minutes:seconds).
#$ -l h_rt=2:0:0

# Request 8 gigabyte of RAM for each core/thread 
# (must be an integer followed by M, G, or T)
#$ -l mem=8G

# Request 10 gigabyte of TMPDIR space
#$ -l tmpfs=10G

# Request 1 GPU
#$ -l gpu=1

# Set the name of the job.
#$ -N stardist-pipeline

# Request 1 cores.
#$ -pe smp 1

# Load python3 module - this must be the same version as loaded when creating and
# installing dependencies in the virtual environment
module load python3/3.9

# Define a local variable pointing to the project directory in your home directory
PROJECT_DIR=$HOME/myriad-stardist-pipeline

# Activate the virtual environment in which you installed the project dependencies
source $PROJECT_DIR/venv/bin/activate

# Change current working directory to temporary file system on node
cd $TMPDIR

# Make a directory save script outputs to
mkdir outputs

# Run pipeline script using Python in activated virtual environment passing in path to
# directory containing input data and path to directory to write outputs to
echo "Running pipeline script..."
python $PROJECT_DIR/compute_stardist_predictions.py \
  --model-dir $PROJECT_DIR/models \
  --image-dir $PROJECT_DIR/images \
  --output-dir outputs
echo "...done."

# Copy script outputs back to scratch space under a job ID specific subdirectory
echo "Copying analysis outputs to scratch space..."
rsync -a outputs/ $HOME/Scratch/outputs_$JOB_ID/
echo "...done"
