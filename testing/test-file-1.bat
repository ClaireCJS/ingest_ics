call setup-test
python ..\ingest_ics.py testdata-1-end_same_day.ics
call pause-on-errorlevel "test 1 failed"
