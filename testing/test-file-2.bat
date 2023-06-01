call setup-test
python ..\ingest_ics.py testdata-2-end_next_day.ics
call pause-on-errorlevel "test 2 failed"
