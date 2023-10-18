import json
import os
import re

class Register_Searcher(object):

    def __init__(self, jsonl=None, ignore_exception=False):
        self.read_line = 1
        self.ignore_exception = ignore_exception
        self._jsonl_db = self.set_jsonl_file(jsonl_file=jsonl)

    def set_jsonl_file(self, jsonl_file=None):
        if jsonl_file is not None and os.path.isfile(jsonl_file):
            jsonl_db = open(jsonl_file, mode="r")
            if jsonl_db is not None and hasattr(jsonl_db, "tell") and hasattr(jsonl_db, "seek"):
                #since the any function call will move the file pointer one position forward, remember it and set it back
                ini_pos = jsonl_db.tell()
                if any(jsonl_db):
                    jsonl_db.seek(ini_pos)
                    return jsonl_db
                else:
                    print("File is empty")
        return None

    def search_json(self, terms=[], allterms=False):
        if any(terms) and self._jsonl_db is not None:
            for entry in self._jsonl_db:
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
        else:
            if not any(terms): print("No terms given")
            if self._jsonl_db is None: print("File not set")

    def search_string(self, terms=[], allterms=False):
        if any(terms) and self._jsonl_db is not None:
            for entry in self._jsonl_db:
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
            if self._jsonl_db is None: print("File not set")

    def search_regex(self, terms=[], allterms=False, ignore_case=False):
        if any(terms) and self._jsonl_db is not None:
            terms_regexes = []
            for term in terms:
                terms_regexes.append(re.compile("" + term + "", flags=0 if not ignore_case else re.IGNORECASE))
            for entry in self._jsonl_db:
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
            if self._jsonl_db is None: print("File not set")
