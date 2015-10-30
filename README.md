# hpweb
A web UI for Hydra Platform

Installation and Setup
======================

To install all the necessary dependencies, you need to run the setup script:

    $ python setup.py develop

If you want to avoid cluttering up your standard python install with all
the turbogears gubbins, then use a virtual environment, described below:

Now edit the development.ini file, changing the following line:
    
    sqlalchemy.url = sqlite:////users/stephen/.hydra/hydra.db

to point to the hydra.db on your machine.

Now visit http://localhost:8081 and log in with the username 'root' and no password.

Setting up a virtual environment
================================

Install ``tgenv`` using the setup.py script:

    $ cd hpweb

Set up the web UI's environment by doing:

    $ . tgenv/bin/activate
    
Start the server (notice the 'tgenv' at the start of the line. this means you 
are in the webUI environment and all the imports will work fine).

    $(tgenv) gearbox serve

While developing you may want the server to reload after changes in package files (or its dependencies) are saved. This can be achieved easily by adding the --reload option::

    $ gearbox serve --reload --debug

Then you are ready to go.o

To leave the web UI's environment:
    
    $deactivate

