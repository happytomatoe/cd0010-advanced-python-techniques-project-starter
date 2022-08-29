CALL python3  -m cProfile -o profile/file1.prof  main.py query --limit 2
CALL python3 -m cProfile -o profile/file2.prof main.py query --date 1969-07-29 --limit 3
CALL python3 -m cProfile -o profile/file3.prof main.py query --start-date 2050-01-01 --limit 3
CALL python3 -m cProfile -o profile/file4.prof main.py query --start-date 2020-03-01 --end-date 2020-03-31 --min-distance 0.4 --limit 4
CALL python3 -m cProfile -o profile/file5.prof main.py query --max-distance 0.0025 --max-velocity 5 --limit 3
CALL python3 -m cProfile -o profile/file6.prof main.py query --start-date 2000-01-01 --min-velocity 15 --min-diameter 6 --limit 3
CALL python3 -m cProfile -o profile/file7.prof main.py query --start-date 2030-01-01 --end-date 2030-01-31 --max-diameter 0.05 --not-hazardous --limit 2
CALL python3 -m cProfile -o profile/file8.prof main.py query --start-date 2021-01-01 --max-distance 0.1 --min-velocity 15 --min-diameter 0.1 --hazardous --limit 3

CALL python3 -m cProfile -o profile/file9.prof main.py query --outfile results.csv

CALL python3 -m cProfile -o profile/file10.prof main.py query --start-date 2020-01-01 --end-date 2029-12-31 --min-diameter 1 --min-distance 0.01 --max-distance 0.1 --outfile results.json