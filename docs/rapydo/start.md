
## debug mode for your development

```bash

rapydo init
# check the status of your scaffold and
# download others repo from the rapydo framework as submodules
[...]

# now you can launch the containers
rapydo start
```

Note: the main backend containers with Flask will be built now if it's the first time you try it. It might take a few minutes, please be patient.

Now open a shell inside the main container and use it

```bash
# check the containers running
rapydo status
# open a shell in the current backend container
rapydo shell backend
# inside the container you can run a flask server in debug mode
$ restapi launch

[...]
# lots of logs
# if you need to stop it use CTRL+C
```
