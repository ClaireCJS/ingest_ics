pushd 
cd ..
set GRAB=update-from-BAT.bat
call validate-environment-variable GRAB
call %GRAB%
popd
