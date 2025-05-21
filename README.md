# Myriad StarDist pipeline

Pipeline for computing image segmentations using [StarDist](https://github.com/stardist/stardist) 
on UCL high performance computing system [Myriad](https://www.rc.ucl.ac.uk/docs/Clusters/Myriad/).

> [!NOTE]
> Make sure you're connected to the UCL network when accessing Myriad either via a UCL VPN or on campus. Alternatively you can [first connect to the UCL SSH gateway](https://www.rc.ucl.ac.uk/docs/howto/#logging-in-from-outside-the-ucl-firewall).
via UCL Eduroam.

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

Transfer required models and images to subdirectories `models` and `images` within `myriad-stardist-pipeline` with
instructions below. The directories should have the following structure:

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

**On your local machine**, you can arrange your files into the above directory structure and zip/compress them
as normal.

You can then [run commands in the shell](https://swcarpentry.github.io/shell-novice/index.html#open-a-new-shell)
to transfer them to the `myriad-stardist-pipeline` directory in your Myriad home directory using `scp`:

```bash
scp models.zip ucaXXXX@myriad.rc.ucl.ac.uk:~/myriad-stardist-pipeline/
scp images.zip ucaXXXX@myriad.rc.ucl.ac.uk:~/myriad-stardist-pipeline/
```

> [!NOTE]
> `ucaXXXX` is your UCL username and this command is similar to `ssh` command you used to connect to Myriad.

**On Myriad**, you can check the contents of your `myriad-stardist-pipeline` directory and any other folder by running the
[ls command](https://swcarpentry.github.io/shell-novice/02-filedir.html):

```bash
cd ~/Scratch
ls
```

You should see the two `.zip` files you just transferred.

> [!TIP]
> You can also check which folder/directory you're currently in by running the `pwd` command.

Next, you need to move the zipped files to the `myriad-stardist-pipeline` directory you created earlier
using the [`mv` command](https://swcarpentry.github.io/shell-novice/03-create.html#moving-files-and-directories
):

```bash
cd ~
mv ~/Scratch/models.zip ~/myriad-stardist-pipeline/
mv ~/Scratch/images.zip ~/myriad-stardist-pipeline/
```

Unzip the files in your `myriad-stardist-pipeline` directory using the `unzip` command:

```bash
cd ~/myriad-stardist-pipeline
unzip models.zip
unzip images.zip
```

You can check the contents of the `models` and `images` directories to confirm that the files have been unzipped correctly:

```bash
cd models
ls
cd ../images
ls
```

Submit job script by running

```bash
cd ~/myriad-stardist-pipeline
qsub job_script.sh
```

On completion the outputs of the job will be written to a directory `outputs_{job_id}` in your `Scratch` space where `{job_id}` is a unique identifier for the job.
