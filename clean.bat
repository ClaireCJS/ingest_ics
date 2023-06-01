@echo off

for %tmpDir in (dist build) do (%COLOR_SUBTLE%  %+ echo - Cleaning: %tmpDir             )
for %tmpDir in (dist build) do (%COLOR_REMOVAL% %+ if isdir %tmpDir (rd  /s /q %tmpDir ))
for %tmpDir in (dist build) do (%COLOR_ALARM%   %+ if isdir %tmpDir (dir /b    %tmpDir*))

%COLOR_NORMAL%


