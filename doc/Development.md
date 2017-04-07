# Development and Testing Guide <br/> Logging Microservice Client SDK for Python

This document provides high-level instructions on how to build and test the microservice.

* [Environment Setup](#setup)
* [Installing](#install)
* [Building](#build)
* [Testing](#test)
* [Contributing](#contrib) 

## <a name="setup"></a> Environment Setup

This is a Python project and you have to install Python 2.7. 
You can download them from official Python website: https://www.python.org/downloads/

After node is installed you can check it by running the following command:
```bash
python --version
```

To work with GitHub code repository you need to install Git from: https://git-scm.com/downloads

If you are planning to develop and test using persistent storages other than flat files
you may need to install database servers:
- Download and install MongoDB database from https://www.mongodb.org/downloads

## <a name="install"></a> Installing

After your environment is ready you can check out microservice source code from the Github repository:
```bash
git clone git@github.com:pip-services-infrastructure/pip-clients-logging-python.git
```

Then go to the project folder and install dependent modules:

```bash
# Install dependencies
pip install -r requirements.txt
```

If you worked with the microservice before you can check out latest changes and update the dependencies:
```bash
# Update source code updates from github
git pull

# Update dependencies
pip update
```

## <a name="test"></a> Testing

Command to run unit tests:
```bash
py.test test -s
```

You can also execute benchmarks as:
```bash
???
```

## <a name="contrib"></a> Contributing

Developers interested in contributing should read the following instructions:

- [How to Contribute](http://www.pipservices.org/contribute/)
- [Guidelines](http://www.pipservices.org/contribute/guidelines)
- [Styleguide](http://www.pipservices.org/contribute/styleguide)
- [ChangeLog](CHANGELOG.md)

> Please do **not** ask general questions in an issue. Issues are only to report bugs, request
  enhancements, or request new features. For general questions and discussions, use the
  [Contributors Forum](http://www.pipservices.org/forums/forum/contributors/).

It is important to note that for each release, the [ChangeLog](CHANGELOG.md) is a resource that will
itemize all:

- Bug Fixes
- New Features
- Breaking Changes