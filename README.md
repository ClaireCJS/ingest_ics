# ics_ingest

ics_ingest creates Google Calendar events from .ics files

## Installation

Just install the appropriate packages, and the script should be ready to go.

```bash
pip install -r requirements.txt
```

## Usage

To monitor a folder (usually c:\calendar) for new ics files:

```python
python ingest_ics.py monitor
```

The process an individual ics file:

```python
python ingest_ics.py some_ic_file
```


## Contributing

Make your own version with neato changes, if you are so inspired.

## License

[The Unlicense](https://choosealicense.com/licenses/unlicense/)

