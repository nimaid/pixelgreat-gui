@echo off

set MAINFAILENAME=pixelgreat-gui
set ENVNAME=%MAINFAILENAME%

set ORIGDIR=%CD%
set SOURCEDIR=%ORIGDIR%\src
set DISTDIR=%ORIGDIR%\dist
set BUILDDIR=%ORIGDIR%\build

set PY=%SOURCEDIR%\%MAINFAILENAME%.py
set SPEC=%ORIGDIR%\%MAINFAILENAME%.spec
set EXE=%DISTDIR%\%MAINFAILENAME%.exe

set VERSION_YAML=%SOURCEDIR%\version.yml
set VERSION_INFO=%ORIGDIR%\file_version_info.txt

set ICON_ICO=%SOURCEDIR%\icon.ico


echo Building portable EXE...
call conda run -n %ENVNAME% create-version-file %VERSION_YAML% --outfile %VERSION_INFO%
if errorlevel 1 goto ERROR
call conda run -n %ENVNAME% pyinstaller ^
    --clean ^
    --noconfirm ^
	--add-data %SOURCEDIR%\*;. ^
    --onefile ^
    --icon=%ICON_ICO% ^
    --version-file=%VERSION_INFO% ^
    "%PY%"
if errorlevel 1 goto ERROR

echo Cleaning up before making release...
move "%EXE%" "%ORIGDIR%"
del /f /s /q "%DISTDIR%" 1>nul 2>&1
rmdir /s /q "%DISTDIR%" 1>nul 2>&1
del /f /s /q "%BUILDDIR%" 1>nul 2>&1
rmdir /s /q "%BUILDDIR%" 1>nul 2>&1
del /f /q "%SPEC%" 1>nul 2>&1
del /f /q "%VERSION_INFO%" 1>nul 2>&1

goto DONE


:ERROR
cd %ORIGDIR%
echo Portable EXE build failed!
exit /B 1

:DONE
cd %ORIGDIR%
echo Portable EXE build done!
exit /B 0