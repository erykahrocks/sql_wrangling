# Requirments

* python@3.7
* psycopg2-binary==2.8.6


# Execution

## Must read preliminaries

Should add `database.ini` file at base directory with following format:

```ini
[postgresql]
host=1.2.3.4
port=5432
database=my_database
user=asdf
password=asdf
```

## Then...

Execute `python query_executor.py --prob \<prob_num\>`

e.x. `python query_executor.py --prob 3`

## For problem 7,

Execute `python main.py`

# Disclaimer

## Random AND non-repeating ID?

### Setting valid range of ID

- Severely damaging "random" part
- Each random number generation results in decreasing set size
- Technically, it's already impaired since BIGINT is already bounded

### Maintaining Hashmap (`random_key -> is_used`)

- Although python maintains memory pretty neat for dict...
- Absurd to have these kind of ugly, heavy variable throughout the session

### :heavy_check_mark: Believe in PK restraint and retry

- Used UUIDv4 for generating 128-bit number and truncated to BIGINT
- Random seed is current system clock, so it's strictly increasing
- If UUIDv4 is duplicated (in chance of lightening), then INSERT query will produce error
- Then retry up to three times with different UUID.
- If all of those retry fails, go buy a lottery!

## SQL query templating

- I used `Template` for filling up values w/ placeholder
- This kind of approach is susceptible to 1. invalid SQL literal 2. security issue
- Better to use SQL string composition already supported in `psycopg2`

## Generalization on problem 7

- Current implementation is only limited to records fetched from specific table
- Introduced `pseudo_user_id` and maintained `pseudo_user_id_map` for duplication check on `person`
- `pseudo_user_id_map` is of course, volatile
- No other choice since every attribute altogether except PK in `person` relationship couldn't be a key

## DROP and CREATE table

* Far from incremental ETL
* Pretty convenient when back-filling the data

## Validation (visit_start_date, drug_exposure_start_date \geq birth_date)

* Comparison only made on `year`
* If visit_start_date is `2021-05-21` and birth_date is `2021-08-03`, validation passes
* Only `year_of_birth` is required attribute

# Assumption made on problem 7

* The very first line of the note is a unique identifier for the patient
* Each note MUST contain person info and visit info (drug and condition is optional)
* Any kind of medical info parsed by single note MUST be associated with the person parsed from the note