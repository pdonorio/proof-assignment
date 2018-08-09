
## pre-requisites

The list of requirements to use the rapydo framework:

1. `git` binary
2. `docker` (daemon/engine and `compose`) to launch containers
3. `python3.4.4+` and `pip3` are required to install the rapydo python packages


## initial setup

Download the repo

```bash
git clone ssh://git@git.proofmedia.io:2222/apps/base-platform.git
cd base-platform
# copy a projectrc to set your defaults from now on
cp templates/debug.rc .projectrc
```

Install (or update) the rapydo controller

```bash
sudo -H pip3 install --upgrade -r requirements.txt
```

<!--

---

Next to read: [startup the framework](docs/rapydo/start.md)
-->
