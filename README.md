# Myriad StarDist pipeline

Pipeline for computing image segmentations using [StarDist](https://github.com/stardist/stardist) 
on UCL high performance computing system [Myriad](https://www.rc.ucl.ac.uk/docs/Clusters/Myriad/).

## How to run pipeline

Clone this repository to your home directory on Myriad

```bash
cd ~
git clone https://github.com/UCL/myriad-stardist-pipeline
cd myriad-stardist-pipeline
```

Load modules with required system level dependencies.
We use a pre-built version of TensorFlow optimized for use with the GPU nodes on Myriad here rather than installing the package separately.
The module versions below are the latest available on Myriad at the time of writing, and the `tensorflow` module comes bundled with a Python 3.9 install.

```bash
module purge
module load compilers/gnu/10.2.0
module load openblas/0.3.13-openmp/gnu-10.2.0
module load tensorflow/2.11.0/gpu
```

Create a Python virtual environment 

```bash
python3 -m venv venv
```

Activate environment, upgrade `pip` and install required Python dependencies

```bash
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Transfer required models and images to subdirectories `models` and `images` within `myriad-stardist-pipeline`. The directories should have the following structure:

```
.
├── images
│   ├── image_1.tif
│   ├── image_2.tif
│   └── ...
└── models
    ├── model_1
    ├── model_2
    └── ...
```

Submit job script by running

```bash
qsub job_script.sh
```

On completion the outputs of the job will be written to a directory `outputs_{job_id}` in your `Scratch` space where `{job_id}` is a unique identifier for the job.
