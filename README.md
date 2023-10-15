Simple search tool for the data in JSONL format from Offene Register
===============

Goes through a JSONL file and searches for given terms in the name of the company and the attributes of the officers of the company.

Usage

```
python3 query_offeneregister.py -j/--jsonl jsonl_file_location [-a/--alterms] search_term [search_term ...]
```

Default search method converts each entry from a JSON formatted string to a Python object and searches for the terms in the company name and attributes of the officers of the company.

-a/--allterms will make the script only return a set of data, if all terms appear in a set
-s/--stringsearch will treat each entry as string and search in there
-r/--regexsearch will convert the term(s) to regular expressions and use them to search the entries
-i/--ignorecase will make the regular expression case insensitive and is only used of -r/--regexsearch is active, otherwise has no effect

Run the tests

```
python3 tests.py
```