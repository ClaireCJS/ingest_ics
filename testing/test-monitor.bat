call setup-test
python ..\ingest_ics.py monitor
call pause-on-errorlevel "monitor test failed"
