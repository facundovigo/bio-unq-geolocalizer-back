## Geolocalizer

### Setup

Recreate the Conda environment from the environment.yml file provided inside this repo:

`conda env create -f environment.yml`

To enable the environment, run: 

`conda activate geolocalizer`

Don't forget to update the YML file if you added new dependencies or updated existing ones by running:

`conda env export > environment.yml`

To update dependencies, run:

`conda env update -n geolocalizer --file environment.yml  --prune`