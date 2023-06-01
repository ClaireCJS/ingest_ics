@Echo off

rem CONFIGURATION: Define project/script.py name:
    set BASENAME=ingest_ics

rem SETUP: Check parameters, set variables, and update our local code to our GIT repository
    set MODE=%1
    set OUR_BUILD_DIR=dist\%BASENAME%
    set CREATED_EXE_FILE=%OUR_BUILD_DIR%\%BASENAME%.exe
    call update-from-BAT

rem BRANCHING: Skip the build if we say to
    set SKIPPED_BUILD=0
    if "%MODE" eq "built" .or. "%MODE" eq "already" .or. "%MODE" eq "post" (
        set SKIPPED_BUILD=1
        goto :built
    )

rem ADVICE: Let us know about some options we may forget about
    call advice if we lose our spec file the timezone bug can likely be fixed by adding --collect-data dateutil to our build optoins here
    call advice rem ember: --onefile, --onedir

rem "MAKE CLEAN": Clean out files from previous builds
    :Make
    call validate-in-path py2exe.bat clean.bat
    call clean.bat

rem "MAKE MAKE": Compile the EXE file ***************************************************************************************
    pushd
    REM optionally add --onedir --onefile here 
    call py2exe.bat %BASENAME%.spec  %*
    popd

rem POST: Double-check EXE was created
    :built
    if not exist %CREATED_EXE_FILE% (
        set MSG=Oops, EXE doesn't exist!
        if %SKIPPED_BUILD eq 1 (call warning %MSG%) 
        else                   (call error   %MSG%)
        if %SKIPPED_BUILD eq 1 (goto :Make)
    )
    call validate-env-var CREATED_EXE_FILE
    echo.
    %COLOR_SUCCESS%
 
rem POST: Create a ZIP file for distribution
    call create-distribution %BASENAME%

