# on se place dans les eaux internationales, loin des quotas
mkdir /tmp/deepl
cd /tmp/deepl

# pour CUDA tensorflow
export LD_LIBRARY_PATH=/applications/matlabr2021b/bin/glnxa64/:$LD_LIBRARY_PATH

# on installe un environnement virtuel python
python3 -m venv .env
source .env/bin/activate
python -m pip install pip tensorflow matplotlib numpy sklearn ipykernel jupterlab

# on inscrit le venv dans la liste des kernels ipython
python -m ipykernel install --user --name=.env

# on lance un notebook
jupyter-lab --no-browser --ip 0.0.0.0 --port 8888