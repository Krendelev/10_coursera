# Coursera Dump

Let's parse 20 random course pages from Cousera and dump their info to `xlsx` file.

## How to Install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

## Usage

```bash
$ python coursera.py
```

Title | Language | Start | Duration | Rating
------------ | ------------- | ------------- | ---------------- | ---------
Strategic Planning and Execution | English, Subtitles: Vietnamese | Sep 27 | 4 | 4.7
Маркетинг инновационных продуктов | Russian | Sep 27 | 7 | 4.9
Afrique et mondialisation, regards croisés | French | Sep 27 | 11 | 4.7
...

## Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
