# COM519 - Garage Booking Application

This application allows the management of garage packages for customers & staff.
It is a python based application with an underlying sqlite database

## Installation

From github download the full repo

```bash
clone https://github.com/murray915/COM519.git
```

Next install all required packages

```bash
pip install -r requirements.txt
```

## Usage

Once downloaded, open main.py and run

To complete test suite before running to ensure all packages are installed, run pytest

```python
pytest -v
```

Note; errors can occur on pytest interactions with ktinker, if "This probably means that Tcl wasn't installed properly." appears, please re-run to confirm clear. This happens as;

- run tests in a different order 
- import modules earlier or later 
- reload Toplevel more than once
- fork worker processes

## Contributing


## License

