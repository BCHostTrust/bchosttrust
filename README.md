# BCHostTrust - Reference Implementation

This repository is the reference implementation of BCHostTrust, a distributed database of domain name trustworthiness. It uses the concept of [blockchain](https://en.wikipedia.org/wiki/Blockchain), a growing list of records linked together via [cryptographic hashes](https://en.wikipedia.org/wiki/Cryptographic_hash_function), in which [SHA3](https://en.wikipedia.org/wiki/SHA-3)-256 is used in BCHostTrust. More detailed information can be found at [documents/tech_paper/README.md](https://github.com/BCHostTrust/documents/blob/master/tech_paper/README.md).

DISCLAIMER: DESPITE USING SIMILAR TECHNOLOGIES, THIS PROJECT IS NOT RELATED TO CRYPTOCURRENCY!

## Installation

To use BCHostTrust, Python 3.11 is required.

### Via pipx (recommended for end users)

In order to use the command-line tool, it is recommended to install it via [pipx](https://pipx.pypa.io/stable/), which runs BCHostTrust in an dedicated virtual environment, isolating it from potential dependency problems. pipx is usually provided via your operating system's package repository, after installing it, run the following command:

```bash
pipx ensurepath  # This ensures pipx is properly configured
pipx install bchosttrust
```

After that, you can run the following command to verify if the installation is working properly:

```console
$ bcht version
BCHostTrust Reference Implementation, version 0.0.0
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

## API Usage

The API of BCHostTrust is well-documented in their respective [docstrings](https://peps.python.org/pep-0257/). Take a look before writing your code on top of BCHostTrust.

All parameters passed into the functions are forced to follow the [hinted type](https://peps.python.org/pep-0484/), thanks to the usage of [typeguard](https://typeguard.readthedocs.io/en/latest/index.html). You should run your code in debug mode (the default in most cases) to see if your code is violating any of the type hints. After that, you may run your well-tested code in optimized mode to avoid performance overheads.

## Contribution

We welcome all kinds of contributions to the BCHostTrust project. You may join in the following ways:

1. **Opening an issue.** This can be either requesting for new features or reporting misbehaviors. By sending feedback to us, we can improve the protocol and the application.
2. **Submiting your codes.** If you are keen on working on codes, you can submit your own by opening a pull request. By doing so, the codebase can be improved collectively.

### Recommended develpoment setup

It is recommended to have the following before starting your journey in development:

1. [Visual Studio Code](https://code.visualstudio.com/), an highly customizable code editor with built-in git integration and a broad of extensions.
2. [Pylint](https://pypi.org/project/pylint/), a [static code analyzer](https://en.wikipedia.org/wiki/Static_code_analysis) that can detect more potential errors and mistakes than other analyzers. It can be integrated into VSCode by the [Pylint extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint).
3. [autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8), an extension of VSCode automatically formats your code to fit the standard as specified in [PEP 8](https://peps.python.org/pep-0008/). It should be configured properly in accordance with its documentation.

To start, create your own fork to work on. Refer to [GitHub's documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks) for how to operate with forks.

After that, clone the repository to your local machine:

```bash
# Using SSH
git clone ssh://git@github.com/[your username]/bchosttrust

# Using GitHub CLI
gh repo clone [your username]/bchosttrust
```

After that, create an virtual environment and install BCHostTrust in [development mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html):

```bash
# Go into BCHostTrust directory
cd bchosttrust

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows

# Install BCHostTrust in develpoment mode
pip install --editable .
```

Done! Now you can work on BCHostTrust. Don't forget to push your changes to your fork and file a pull request.

## Roadmap

- [x] Prototype
  - [x] Blockchain Core
  - [x] Basic Proof-of-work Mechanism
  - [x] Chain Search and Analysis
  - [x] Command-line client
- [ ] Configuration file for command-line
- [ ] Block exchange protocol
- [ ] Browser integration (probably in dedicated repository)
