# Xuproc - JUnit XML file processing script

Purpose of this Python script is to prepend classname to method name for each test case in JUnit XML file.

## Installation
1. Clone this repository to your local machine.
    ```bash
    git clone https://github.com/Tem12/xuproc.git
    ```

2. Create python venv and install dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage
```
usage: xuproc.py [options] [file]

JUnit XML file processing script. Prepend classname to method name for each test case.

positional arguments:
  file        File to process

options:
  -h, --help  show this help message and exit
  -j          Update each test case in the file
```

## Error codes implementation
Scripts uses different exit code for different program error:

|Definition|Code|Description|
|-|-|-|
| EXIT_FAILURE_PARSE | 10 | Invalid XML structure which cannot be parsed. |
| EXIT_FAILURE_FILE_NOT_FOUND | 11 | Input file cannot be found. |
| EXIT_FAILURE_FILE_PERMISSIONS | 12 | Missing permissions to input. |
| EXIT_FAILURE_ARG | 13 | File argument provided but `-j` flag is missing. |
| EXIT_FAILURE_CLASSNAME | 14 | Missing `classname` in input XML file. |
| EXIT_FAILURE_NAME | 15 | Missing `name` in input XML file. |
| EXIT_FAILURE_OTHER | 100 | Other runtime exception. |

Note that there might also be other error codes produced by invalid program arguments.

## Testing
To test the script, use pytest which is included in the requirements.

```
pytest
```