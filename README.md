# csv_parser
## Usage
`csv_parser [CSV file] [column to sort]`

If no CSV file is specified then `csv_parser` expects CSV data from STDIN and must be interrupted if no data is provided.
csv_parser may be run either directly:

`./csv_parser Period < overseas-trade-indexes-June-2021-quarter-provisional-csv.csv`

## Samples
Two basic samples are included.
### test.csv
This file is the "most complicated" CSV example from [Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values).
The columns in this file are:
 * Year
 * Make
 * Model
 * Description
 * Price
### test2.csv
A basic CSV example
The columns in this file are:
 * City
 * State
 * Motto
 * Mayor
### overseas-trade-indexes-June-2021-quarter-provisional-csv.csv
Sourced from [https://www.stats.govt.nz/large-datasets/csv-files-for-download/](https://www.stats.govt.nz/assets/Uploads/International-trade/International-trade-June-2021-quarter/Download-data/overseas-trade-indexes-June-2021-quarter-provisional-csv.csv)
The columns in this file are:
 * Series_reference
 * Period
 * Data_value
 * STATUS
 * UNITS
 * MAGNTUDE
 * Subject
 * Group
 * Series_title_1
 * Series_title_2
 * Series_title_3
 * Series_title_4
 * Series_title_5

## Docker
A Dockerfile is included to enable building a Docker image and running csv_parser as a Docker container

 1. `docker build --tag="csv_parser:latest" .`
 2. `docker run -i --rm csv_parser Period < overseas-trade-indexes-June-2021-quarter-provisional-csv.csv`

## Cucumber
A sample Gherkin file is included to facilitate validating csv_parser