@Echo OFF

REM        USAGE: pack-zip BASENAME [basename of the .py/our project name]


REM SETUP: Get/Generate base name        
        if "%BASENAME%" eq ""(set BASENAME=%@NAME[%_CWD]) else (set BASENAME=%1)

REM CONFIGURATION: Set ZIP & BAT filenames, distribution dir name, delete command
        set  DISTRIBUTION_DIR=dist
        set  BAT_FILE=%DISTRIBUTION_DIR%\runme.bat
        set  DELETE_COMMAND=*del

REM Create a BAT file that runs our EXE file
        call validate-env-var BASENAME 
        call validate-env-var BAT_FILE skip_validation_existence
        call validate-in-path important celebration errorlevel
        echo.
        call important * Creating bat file: %BAT_FILE%
        echo %BASENAME%\%BASENAME%.exe     >%BAT_FILE%

REM Create ZIP file for distribution
        set ARCH=unknow_architecture
        if  0 eq  %_X64  (set ARCH=x86)
        if  1 eq  %_X64  (set ARCH=x64)
        set ZIP_FILENAME=%BASENAME%-%@LOWER[%_DOS]-%_DOSVER-%ARCH%.zip
        call important * Creating zip file: %ZIP_FILENAME%
        call validate-env-var DISTRIBUTION_DIR DELETE_COMMAND
        cd %DISTRIBUTION_DIR%            
        set ZIP_DIR=..
            set ZIP_NAME=%ZIP_DIR%\%ZIP_FILENAME%
            if exist "%ZIP_NAME%" (%COLOR_REMOVAL% %+ %DELETE_COMMAND% "%ZIP_NAME%")
            set ZIP_COMMAND_ADD=*zip /A /R "%ZIP_NAME%" .\*.* %BASENAME%\*.*
            call validate-env-var ZIP_DIR
            %COLOR_SUCCESS%
            %ZIP_COMMAND_ADD%
            echo.
            call errorlevel  "* Creating zip distribution failed" 
            call celebration "*** Zip distribution %ZIP_FILENAME% successfully created! ***"
            call validate-env-var ZIP_NAME
        cd ..
        call validate-env-var ZIP_FILENAME
        echo.
        %COLOR_IMPORTANT_LESS%
        dir /k /m            %ZIP_FILENAME%

REM 


REM Cleanup
    set BASENAME=


