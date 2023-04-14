# Parser of economic metrics
Parser of economic indicators of the top 400 Russian companies

## Usage
Install reqs first
```
python3.9 -m pip install requirements.txt
```

Basic run
```
python3.9 -m parser
```

Runnable options
```
python3.9 -m parser --help
```

Upload by years period in range `[2013, 2021]`. Default is `--start-year=2013`, `--end-year=2021`.
```
python3.9 -m parser --start-year=2013 --end-year=2021
```

Also could be created sdist and installed as package:
```
make sdist
python3.9 -m pip install dist/*.tar.gz
```
