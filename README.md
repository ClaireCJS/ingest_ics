# ics_ingest

ics_ingest creates Google Calendar events from .ics files

When running in monitor mode, simply save .ics files into your c:\calendar folder, and a new browser window will open up to a Google Calendar event creation page.

When running in single file mode, siply provide an .ics filename as a command-line argument, and a new browser window will open up to a Google Calendar event creation page.

## Installation

Just install the appropriate packages, and the script should be ready to go.

```bash
pip install -r requirements.txt
```

## Usage

To monitor a folder (usually c:\calendar) for new ics files saved into that folder:

```python
python ingest_ics.py monitor
```

The process an individual ics file:

```python
python ingest_ics.py event.ics
```


## Contributing

Make your own version with neato changes, if you are so inspired.

## License

[The Unlicense](https://choosealicense.com/licenses/unlicense/)

