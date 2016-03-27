#Python Client Library for Nunace OmniPage Server

Client library for Nuance OmniPage Server written in Python.

  [![NPM Version][npm-image]][npm-url]
  [![NPM Downloads][downloads-image]][downloads-url]
  [![Linux Build][travis-image]][travis-url]
  [![Windows Build][appveyor-image]][appveyor-url]
  [![Test Coverage][coveralls-image]][coveralls-url]

## Requirement
Nuance OmniPage Server

## Install

```bash
$ pip install git+https://github.com/bandetech/opsclient-python.git
```

## Sample
Please see samples/libTest.py

## Limitation
* Authentication is not implemented.
* There are some unimplemented methods.
  * CreatePreallocatedJob
  * ProcessOnCall
  * SetJobDataDescription
  * CreateLocalJob