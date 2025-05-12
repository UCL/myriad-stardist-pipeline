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

Create a Python 3.9 virtual environment

```bash
module load python3/3.9
python -m venv venv
```

Activate environment and install required dependencies

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
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
