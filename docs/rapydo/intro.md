
# rapydo

## quick intro to the framework behind this exercise

`RAPyDo` is an open-source framework, currently used for many (internal) projects. We are in the process of evaluating how to write tutorials and documentation to bring people to join the effort.

It was initially written to help the use of docker containers to non-DevOps engineers while developing a typical web application based on: 
- backend APIs
- JS frontend 
- a gateway/proxy to access

## just a matter of configuration

Taking advantage of `docker-compose` we splitted base and custom configuration to:
- keep best practices on many services
- easily switch from debugging/developing to production mode 
- keep simple access to services (db, internal/external servers, etc.) from backend
- keep simple access from frontend to backend

NOTE: in this exercise you will only play with `debug` mode for simplicity.

## how it works

The rapydo framework requires a `controller` installed locally through a python package to do the work for you. When you have that you can launch commands from terminal starting with `rapydo` binary, e.g.

```bash
$ cd path/to/your/rapydo/project
$ rapydo start
```

To fullfil rapydo requirements your repository needs to meet some folders pattern. 
So we prepared a scaffold for you with a preset configuration with:
- backend container with Python3 and Flask installed and configured
- mongodb server container connected to the backend container

From this scaffold it would be easy to add a react or angular frontend, and switch to deploy in production with almost zero changes.
