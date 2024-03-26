import asyncio
import json
import sys
from datetime import datetime
from dotenv import load_dotenv
from aipassyou.argparser import parse_args
from aipassyou.data import Scan
from aipassyou.social.twitter import Twitter
from aipassyou.social.instagram import Instagram
from aipassyou.social.facebook import Facebook
from aipassyou.ai import search
from aipassyou.dictionary import Generator

def model_to_file(scan, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(scan.model_dump_json(exclude_none=True))

def model_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return Scan.model_validate_json(f.read())

def json_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def json_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def scanner(args):
    scan = Scan(args = sys.argv)
    scan.start_date = datetime.now()

    if args.twitter: # IbaiLlanos
        print("[*] Loading information from Twitter profile '{}'... ".format(args.twitter), end="")
        t = Twitter(args.twitter)
        asyncio.run(t.extract(args.npost))
        scan.results.append(t.data)
        print(" Done!")

    if args.instagram: # 'ibaillanos'
        print("[*] Loading information from Instagram profile '{}'... ".format(args.instagram), end="")
        scan.results.append(Instagram(args.instagram).extract(args.npost))
        print(" Done!")
    
    if args.facebook:
        print("[*] Loading information from Facebook profile '{}'... ".format(args.facebook), end="")
        scan.results.append(Facebook(args.facebook).extract(args.npost))
        print(" Done!")
    
    scan.end_date = datetime.now()

    return scan

def main():
    load_dotenv()
    args = parse_args()

    if args.lkwords: 
        kwords = json_from_file(args.lkwords)
    else:
        if args.ldata:
            scan = model_from_file(args.ldata)
        else:
            scan = scanner(args)
            if len(scan.results) == 0:
                print("[!] No data extracted from social networks")
                sys.exit()
            if args.sdata: model_to_file(scan, args.sdata)

        if args.debug:
            print("[DEBUG] Data: \n")
            print(scan)
        
        kwords = search(scan, args.model, args.temperature, args.nkeywords)
        if args.skwords: json_to_file(kwords, args.skwords)
    
    if args.keywords: kwords['custom'] = args.keywords.split(',')
    
    if args.debug:
        print("[DEBUG] AI Keywords: \n")
        print(kwords)
    
    Generator(kwords, args.output).generate()
    
    
if __name__ == "__main__":
    main()