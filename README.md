# Project : Sondesh 

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
![Maintainer](https://img.shields.io/badge/maintainer-Koushik-blue)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/release-1.0-green.svg)](https://shields.io/)
<br>
![logo.png](https://ibb.co/q1qpv5j)

## Description

Sondesh is the name of my cat . I love him very much 
so i've decided to name this project after him.

This project is all about a parser and comparator . 
Question is what it is parsing ? 
- It parse SQL statements , but only DDL statements
- It supports many sql dialects , example oracle , postgresql , sparksql , hive .. 
- There is a cli app ( cli_app.py ), it compares two DDL statements and show you the differences in terminal

## How to use the cli app ? 

```commandline
python cli_app.py
```
- Then just follow the instruction in the terminal 
- You either paste the raw sql or paste any absolute / relative path of sql file

![compare_result.png](https://ibb.co/pKRddz4)

### Dependencies

* Windows 10 , Debian , BSD these are the supported platform 
* Python version >=  3.8

### Installing

* ddl_compare can be installed using pip 

```
pip install ddl-parse
```

### Usage

```python
from ddlparser import ddl_parser
import pprint

result = ddl_parser.parse_from_file('/home/koushik/sample_ddl.sql')
pprint.pprint(result)
``` 

Using the CLI APP . 

1. Just Open the Terminal 
2. type sondesh
3. VOALAA !!!!! 

![logo_terminal.png](https://ibb.co/zsfmN0L)

## What Next :

1. Integration to remote file system to load .sql from there and parse it
2. Integration with data-catalogues like spark catalogue or hive metastore and compare ddl.



