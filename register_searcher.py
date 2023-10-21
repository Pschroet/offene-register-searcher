from enum import Enum
import json
import os
import re

class Compare_Mode(Enum):
    json = 0
    string = 1
    regex = 2

class Register_Searcher():


    def __init__(self, jsonl=None, ignore_exception=False, offset=0):
        self.read_line = 1 if offset is None or offset < 1 else  offset
        self.ignore_exception = ignore_exception
        self._jsonl_db = self.set_jsonl_file(jsonl_file=jsonl, offset=offset)

    def set_jsonl_file(self, jsonl_file=None, offset=0):
        if jsonl_file is not None and os.path.isfile(jsonl_file):
            jsonl_db = open(jsonl_file, mode="r")
            if jsonl_db is not None and hasattr(jsonl_db, "tell") and hasattr(jsonl_db, "seek"):
                #since the any function call will move the file pointer one position forward, remember it and set it back
                ini_pos = jsonl_db.tell()
                if any(jsonl_db):
                    jsonl_db.seek(ini_pos)
                    if offset is not None and offset > 0:
                        for _ in range(0, offset):
                            next(jsonl_db)
                    return jsonl_db
                else:
                    print("File is empty")
        return None

    def search(self, compare_mode=None, terms=[], allterms=False, **kwargs):
        if compare_mode is not None and compare_mode == Compare_Mode.regex:
            self.terms_regexes = []
            for term in terms:
                self.terms_regexes.append(re.compile("" + term + "", flags=re.IGNORECASE if "ignore_case" in kwargs and kwargs["ignore_case"] else 0))
        if any(terms) and self._jsonl_db is not None:
            for entry in self._jsonl_db:
                match compare_mode:
                    case Compare_Mode.json:
                        self._search_json(entry=entry, terms=terms, allterms=allterms)
                    case Compare_Mode.string:
                        self._search_string(entry=entry, terms=terms, allterms=allterms)
                    case Compare_Mode.regex:
                        self._search_regex(entry=entry, terms=terms, allterms=allterms)
        else:
            if not any(terms): print("No terms given")
            if self._jsonl_db is None: print("File not set")

    def _search_json(self, entry="", terms=[], allterms=False):
        try:
            allterms_found = True
            entry_data = json.loads(entry)
            for t in terms:
                term_found = False
                if (("name" in entry_data and t in entry_data["name"]) or
                    ("registered_address" in entry_data and t in entry_data["registered_address"]) or
                    ("all_attributes" in entry_data and "federal_state" in entry_data["all_attributes"] and t in entry_data["all_attributes"]["federal_state"]) or
                    ("all_attributes" in entry_data and "registered_office" in entry_data["all_attributes"] and t in entry_data["all_attributes"]["registered_office"]) or
                    ("all_attributes" in entry_data and "registrar" in entry_data["all_attributes"] and t in entry_data["all_attributes"]["registrar"])):
                    term_found = True
                elif "officers" in entry_data:
                    for o in entry_data["officers"]:
                        if "name" in o and t in o["name"]:
                            term_found = True
                            break
                        if "other_attributes" in o:
                            for officer_attribute in o["other_attributes"]:
                                if isinstance(o["other_attributes"][officer_attribute], str) and t in o["other_attributes"][officer_attribute]:
                                    term_found = True
                                    break
                if not allterms and term_found:
                    print("Found term '" + str(t) + "' in line " + str(self.read_line) + ": " + str(entry_data))
                    #exit loop, because one term has been found, which is enough
                    break
                elif not term_found:
                    allterms_found = False
                    #all terms required, it's enough that one hasn't been found
                    break
            if allterms and allterms_found:
                print("Found all terms " + str(terms) + " in line " + str(self.read_line) + ": " + str(entry_data))
            self.read_line += 1
        except Exception as e:
            print("Error in data in line " + str(self.read_line) + ":" + os.linesep + "-> " + str(entry))
            if self.ignore_exception:
                print(str(e))
            else:
                raise

    def _search_string(self, entry="", terms=[], allterms=False):
        allterms_found = True
        for t in terms:
            term_found = True if t in entry else False
            if not allterms and term_found:
                print("Found term '" + str(t) + "' in line " + str(self.read_line) + ": " + str(entry))
                #exit loop, because one term has been found, which is enough
                break
            elif not term_found:
                allterms_found = False
                #all terms required, it's enough that one hasn't been found
                break
        if allterms and allterms_found:
            print("Found all terms " + str(terms) + " in line " + str(self.read_line) + ": " + str(entry))
        self.read_line += 1

    def _search_regex(self, entry="", terms=[], allterms=False):
        allterms_found = True
        for tr in self.terms_regexes:
            #search returns the position of the first hit or None, so check if the return value is not None
            term_found = tr.search(entry) is not None
            if not allterms and term_found:
                print("Found term '" + str(tr) + "' in line " + str(self.read_line) + ": " + str(entry))
                #exit loop, because one term has been found, which is enough
                break
            elif not term_found:
                allterms_found = False
                #all terms required, it's enough that one hasn't been found
                break
        if allterms and allterms_found:
            print("Found all terms " + str(terms) + " in line " + str(self.read_line) + ": " + str(entry))
        self.read_line += 1
