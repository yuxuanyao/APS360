export CONDA_ENV_NAME=aps360_project
echo $CONDA_ENV_NAME

conda create -n $CONDA_ENV_NAME python=3.6.9

eval "$(conda shell.bash hook)"
conda activate $CONDA_ENV_NAME

pip install gdown