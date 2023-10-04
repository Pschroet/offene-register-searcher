import json
import os

class Register_Searcher(object):

    def __init__(self, jsonl=None, ignore_exception=False):
        self.jsonl = jsonl
        self.jsonl_db = open(self.jsonl, mode="r")
        self.read_line = 1
        self.ignore_exception = ignore_exception

    def search(self, terms=[], allterms=False):
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