import argparse
import os
from register_searcher import Register_Searcher, Compare_Mode

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("terms", default=[], nargs="+", help="terms to search for in the data")
    argparser.add_argument("-j", "--jsonl", required=True, action="store", default=None, help="file to serve as database")
    argparser.add_argument("-a", "--allterms", action="store_true", default=False, required=False, help="line must contain all search terms")
    argparser.add_argument("-s", "--stringsearch", action="store_true", default=False, required=False, help="search lines with string comparison")
    argparser.add_argument("-r", "--regexsearch", action="store_true", default=False, required=False, help="search lines with regular expressions")
    argparser.add_argument("-i", "--ignorecase", action="store_true", default=False, required=False, help="ignore cases, argument will be ignored if -r/--regexsearch is not active")
    argparser.add_argument("-o", "--offset", required=False, action="store", type=int, default=0, help="offset for the file pointer")
    argparser.add_argument("-e", "--end", required=False, action="store", type=int, default=0, help="end before given line")
    args = argparser.parse_args()
    if not hasattr(args, "jsonl") or args.jsonl is None:
        print("argument jsonl file is missing, usage")
        print(argparser.format_usage())
    else:
        if not os.path.isfile(args.jsonl):
            print("file " + str(args.jsonl) + " not found")
        else:
            try:
                print("Searching for terms " + str(args.terms) + " in database " + str(args.jsonl))
                reg_par = Register_Searcher(jsonl=args.jsonl, offset=args.offset, end=args.end)
                if args.stringsearch: reg_par.search(compare_mode=Compare_Mode.string, terms=args.terms, allterms=args.allterms)
                elif args.regexsearch: reg_par.search(compare_mode=Compare_Mode.regex, terms=args.terms, allterms=args.allterms, ignore_case=args.ignorecase)
                else: reg_par.search(compare_mode=Compare_Mode.json, terms=args.terms, allterms=args.allterms)
            finally:
                reg_par._jsonl_db.close()
