import json
import os
import re

class Register_Searcher(object):

    def __init__(self, jsonl=None, ignore_exception=False):
        self.jsonl_db = open(jsonl, mode="r") if jsonl is not None and os.path.isfile(jsonl) else None
        self.read_line = 1
        self.ignore_exception = ignore_exception

    def search_json(self, terms=[], allterms=False):
        if self.jsonl_db is not None and hasattr(self.jsonl_db, "tell") and hasattr(self.jsonl_db, "seek"):
            #since the any function call in the second if will move the file pointer one position forwards, remember it and set it back
            ini_pos = self.jsonl_db.tell()
            if any(terms) and self.jsonl_db is not None and any(self.jsonl_db):
                self.jsonl_db.seek(ini_pos)
                for entry in self.jsonl_db:
                    try:
                        allterms_found = True
                        entry_data = json.loads(entry)
                        for t in terms:
                            term_found = False
                            if "name" in entry_data and t in entry_data["name"]:
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
            else:
                if not any(terms): print("No terms given")
                if not any(self.jsonl_db): print("File is empty")
        elif self.jsonl_db is None:
            print("No JSONL file set")

    def search_string(self, terms=[], allterms=False):
        if self.jsonl_db is not None and hasattr(self.jsonl_db, "tell") and hasattr(self.jsonl_db, "seek"):
            #since the any function call in the second if will move the file pointer one position forwards, remember it and set it back
            ini_pos = self.jsonl_db.tell()
            if any(terms) and self.jsonl_db is not None and any(self.jsonl_db):
                self.jsonl_db.seek(ini_pos)
                for entry in self.jsonl_db:
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
            else:
                if not any(terms): print("No terms given")
                if not any(self.jsonl_db): print("File is empty")
        elif self.jsonl_db is None:
            print("No JSONL file set")

    def search_regex(self, terms=[], allterms=False, ignore_case=False):
        if self.jsonl_db is not None and hasattr(self.jsonl_db, "tell") and hasattr(self.jsonl_db, "seek"):
            #since the any function call in the second if will move the file pointer one position forwards, remember it and set it back
            ini_pos = self.jsonl_db.tell()
            if any(terms) and self.jsonl_db is not None and any(self.jsonl_db):
                self.jsonl_db.seek(ini_pos)
                terms_regexes = []
                for term in terms:
                    terms_regexes.append(re.compile("" + term + "", flags=0 if not ignore_case else re.IGNORECASE))
                for entry in self.jsonl_db:
                    allterms_found = True
                    for tr in terms_regexes:
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
            else:
                if not any(terms): print("No terms given")
                if not any(self.jsonl_db): print("File is empty")
        elif self.jsonl_db is None:
            print("No JSONL file set")
