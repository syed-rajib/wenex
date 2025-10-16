**wenex Backend**
Pre requisites
1. Install Docker
To run this project with a docker command, we have to install Docker Engine and Docker Compose on our local machine.

2. Install Pyenv
For development purpose you have to install python interpreter of multiple versions as a different project use a different version. To do so you can use pyenv.

3. Install Poetry
We are using Poetry for package management tools. We are using this to create virtualenv as well.

If you want to use poetry with pyenv locally and want to ensure that both tools are using the same python version, run the following command before running any poetry command.

poetry env use $(pyenv which python)
