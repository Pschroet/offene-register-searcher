Simple search tool for the data in JSONL from Offene Register
===============

Goes through a JSONL file and searches for given terms in the name of the company and the attributes of the officers of the company.

Usage

```
python3 query_offeneregister.py -j jsonl_file_location [-a/--alterms] search_term [search_term ...]
```

-a/--allterms will make the script only return a set of data, if all terms appear in a set

Run the tests

```
python3 tests.py
```l