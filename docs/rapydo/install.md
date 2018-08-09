
## pre-requisites

The list of requirements to use the rapydo framework:

1. `git` binary
2. `docker` (daemon/engine and `compose`) to launch containers
3. `python3.4.4+` and `pip3` are required to install the rapydo python packages


## initial setup

Download the repo

```bash
git clone https://github.com/GIT_LINK mytask
cd mytask
```

Install (or update) the rapydo controller

```bash
sudo -H pip3 install --upgrade -r requirements.txt
```

Check if it works:
```bash
rapydo version
```

<!--

---

Next to read: [startup the framework](docs/rapydo/start.md)
-->
