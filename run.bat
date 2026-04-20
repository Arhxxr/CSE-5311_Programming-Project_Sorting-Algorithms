@echo off
title 5311- Programming Project - Arham Shams Sameer - 1002078834- Sorting Algorithms
cd /d "%~dp0"

echo.
echo ============================================================
echo   5311- Programming Project - Sorting Algorithms           ^|
echo   Arham Shams Sameer - 1002078834                          ^|
echo   04/17/2026                                               ^|
echo ============================================================
echo.

:: activate venv
if exist venv\Scripts\activate.bat (call venv\Scripts\activate.bat) else (echo [!] No venv found. Using system Python.)

echo ============================================================
echo   STEP 1/4: Running self-test on all 7 algorithms          ^|
echo ============================================================
echo.
python src\sorting_algorithms.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Self-test failed! check sorting_algorithms.py.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   STEP 2/4: Generating input files (24 files)              ^|
echo ============================================================
echo.
python src\input_generator.py
echo.
echo   -^> Check: inputs\ directory for 24 .txt files
echo      (6 sizes x 4 distributions: random, sorted, reverse, nearly)
echo.

echo ============================================================
echo   STEP 3/4: Running benchmark                              ^|
echo ============================================================
echo.
python src\benchmark.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Benchmark failed!
    pause
    exit /b 1
)
echo.
echo ============================================================
echo   RESULTS                                                  ^|
echo ============================================================
echo.
echo   Raw data:   results\benchmark_results.csv
echo   Charts:     results\chart_*.png (10 PNG files)
echo   Report:     docs\project_report.pdf
echo.
echo   Charts generated:
echo     - chart_random.png / chart_random_log.png
echo     - chart_sorted.png / chart_sorted_log.png
echo     - chart_reverse.png / chart_reverse_log.png
echo     - chart_nearly.png / chart_nearly_log.png
echo     - chart_fast_only.png (O(n log n) algorithms only)
echo     - chart_quicksort_comparison.png (regular vs median-3)
echo.
echo ============================================================
echo   STEP 4/4: Launching GUI (bonus deliverable)              ^|
echo ============================================================
echo.
echo   The GUI window should open now.
echo   - Select algorithms, set input size, select distribution
echo   - Press "Run Benchmark" to see results + bar chart
echo.
python src\gui.py

echo.
echo ============================================================
echo  THE END!                                                  ^|
echo ============================================================
echo.
pause
