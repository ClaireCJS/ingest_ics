# ics_ingest

ics_ingest makes it so Google Calendar events are created from any ics files saved on your computer

## What are ics files?

ics files: 

* are calendar files 

* represent an event

* can add events to your calendar

* are the ONLY way certain websites export their events

* don't work well on PCs

* can be handled by certain browser plugins (but those plugins are usually written to handle links)



## Installation: Python

Just install the appropriate packages, and the script should be ready to go.

```bash
pip install -r requirements.txt
```

 ## Installation: Windows 10 EXE: Quick Start instructions

* **Quick Start: Click [here](http://github.com/ClioCJS/ingest_ics/raw/main/ingest_ics-windows10-10.0-x64.zip) or [here](http://github.com/ClaireCJS/ingest_ics/raw/main/ingest_ics-windows10-10.0-x64.zip) to download, unzip, click "runme", start saving ics files into c:\calendar**

 ## Installation: Windows 10 EXE: Detailed instructions

* Download the Windows 10 binary executable from:
    * [here](http://github.com/ClioCJS/ingest_ics/raw/main/ingest_ics-windows10-10.0-x64.zip)
    * [or here](http://github.com/ClaireCJS/ingest_ics/raw/main/ingest_ics-windows10-10.0-x64.zip)

* Unzip the ZIP file
    * Make sure you're unzipping the whole thing and not just the files in the top folder ;)
    * Unzip it somewhere permanent
        * like your desktop
        * or "c:\Program Files"
        * or "c:\calendar", since this will create that folder anyway

* Double-click the "runme.bat" file to run 

* Start saving .ics files into c:\calendar and watch your web browser auto-open with Google Calendar event creation tabs

## Usage: Monitor mode / Service mode

To monitor a folder (c:\calendar by default) for new ics files saved into that folder, simply run the program with no options, or double-click the EXE (if you have one):

```python
python ingest_ics.py
```

Note that this will create the monitor folder if it doesn't exist, but it will also mention this on the screen so you will know.


## Usage: File mode

To process a single ics file:

```python
python ingest_ics.py <some_filename.ics>
```

This will process a single ics file.  This is useful for testing, batch scripting, or if you have a user saving these .ics files on a network share so that they can be processed later on a different machine.

## Why not just use a browser plugin?

Some websites let you export events to your calendar.

But some force a download of ics files, rather than providing a link to one. 

Browser plugins for ics files are usually designed to process links (at least, the ones I looked at).

What is needed is an endpoint on our PC that processes these files. 

This is that endpoint solution.

## Contributing: Compiling

I absolutely would love to have other people -- as long as you don't live in the GMT timezone -- to compile versions for architectures other than my own (Windows 10). Just make sure to check that your event times are properly translating, first.  The GMT-offset bug in compiled EXEs requires modification in the spec file to work.  Mine can be seen [here](https://github.com/ClioCJS/ingest_ics/blob/main/ingest_ics.spec)

## Contributing: Modification

Feel free to make your own version with neato changes, if you are so inspired.

## Those wacky BAT files?

I use TCC -- Take Command Command Line.
Technically, my .BAT files are .BTM files.
If you want to get the ones I have working, contact me, I can help.

## License

[The Unlicense](https://choosealicense.com/licenses/unlicense/)

