Feature: Validate csv_parser

  Scenario Outline: Validate csv_parser's sorting
    Given a CSV file and column name:
    When csv_parser opens <filename> and sorts by <column>
    Then the first value in column should be <firstValue>
    And the last value in colum should be <lastValue>

    Examples:
      | filename | column | firstValue     | lastValue                      |
      | test.csv | Year   | 1999           | 1996                           |
      | test.csv | Make   | Jeep           | Chevy                          |
      | test.csv | Model  | Grand Cherokee | "Venture ""Extended Edition""" |
      | test.csv | Price  | 5000.00        | 3000.00                        |
