# hpweb
A web UI for Hydra Platform

Installation and Setup
======================

Install ``hpweb`` using the setup.py script::

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
