# on se place dans les eaux internationales, loin des quotas
# hint: le dossier work est le disque dur de la machine, dispo en publique à tout le monde
# il faut alors se connecter à la même machine si l'on souhaite accéder à ces fichiers
mkdir /work/$USER-deepl
cd /work/$USER-deepl

# linking CUDA pour tensorflow (pas du tout volé à matlab)
export LD_LIBRARY_PATH=/applications/matlabr2021b/bin/glnxa64/:$LD_LIBRARY_PATH

# on installe un environnement virtuel python
python3 -m venv .env
source .env/bin/activate
python -m pip install pip tensorflow matplotlib numpy sklearn ipykernel jupyterlab pandas pretty_confusion_matrix albumentations

# on inscrit le venv dans la liste des kernels ipython
python -m ipykernel install --user --name=.env

# on lance un notebook
jupyter-lab --no-browser --ip 0.0.0.0 --port 8888 --NotebookApp.token='tokendemerde'
