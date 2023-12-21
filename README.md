# BCHostTrust - Reference Implementation

This repository is the reference implementation of BCHostTrust, a distributed database of domain name trustworthiness. It uses the concept of [blockchain](https://en.wikipedia.org/wiki/Blockchain), a growing list of records linked together via [cryptographic hashes](https://en.wikipedia.org/wiki/Cryptographic_hash_function), in which [SHA3](https://en.wikipedia.org/wiki/SHA-3)-256 is used in BCHostTrust.

## Installation

To use BCHostTrust, at least Python 3.11 is required.

### Via pipx (recommended for end users)

In order to use the command-line tool, it is recommended to install it via [pipx](https://pipx.pypa.io/stable/), which runs BCHostTrust in an dedicated virtual environment, isolating it from potential dependency problems. pipx is usually provided via your operating system's package repository, after installing it, run the following command:

```bash
pipx ensurepath  # This ensures pipx is properly configured
pipx install bchosttrust
```

After that, you can run the following command to verify if the installation is working properly:

```bash
bcht version
# BCHostTrust Reference Implementation, version 0.0.0
```

### Via pip (recommended for application developers)

To import BCHostTrust into your projects, install the package via pip after activating the [virtual environment](https://docs.python.org/3/library/venv.html):

```bash
pip install bchosttrust
```

After that, run the following in a Python console to verify the installation:

```pycon
>>> import bchosttrust
>>> bchosttrust.__version__
"0.0.0"
```

Installing BCHostTrust directly user-wide or system-wide is discouraged as it may cause conflicts between versions or system packages.
