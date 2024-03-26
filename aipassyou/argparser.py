import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog="AIPassYou,py", add_help=False)
    
    social_group = parser.add_argument_group('Social network options')
    social_group.add_argument("-i", "--instagram", dest="instagram", help="Instagram username")
    social_group.add_argument("-t", "--twitter", dest="twitter", help="Twitter username")
    social_group.add_argument("-f", "--facebook", dest="facebook", help="Facebook username")
    social_group.add_argument("-l", "--linkedin", dest="linkedin", help="LinkedIn username")
    social_group.add_argument("--num-posts", dest="npost", help="Number of posts to load from Social Networks (default: 20)", type=int, default=20)

    ai_group = parser.add_argument_group('ChatGPT options')
    ai_group.add_argument("--temperature", dest="temperature", help="ChatGPT temperature (default: '0.2')", type=float, default=0.2)
    ai_group.add_argument("--model", dest="model", help="ChatGPT model (default: 'gpt-3.5-turbo')", default='gpt-3.5-turbo')
    ai_group.add_argument("--num-keywords", dest="nkeywords", help="Number of keywords for each question (default: 5)", type=int, default=5)

    io_group = parser.add_argument_group('Input/output options')
    io_group.add_argument("-o", "--output", dest="output", help="Wordlist output file (default to stdout)")
    io_group.add_argument("--save-data", dest="sdata", help="Save social networks information to JSON file")
    io_group.add_argument("--load-data", dest="ldata", help="Load social networks information from JSON file")
    io_group.add_argument("--save-keywords", dest="skwords", help="Save AI generated keywords to JSON file")
    io_group.add_argument("--load-keywords", dest="lkwords", help="Load AI generated keywords from JSON file")

    wordlist_group = parser.add_argument_group('Wordlist options')
    wordlist_group.add_argument( "-k", "--keywords", dest="keywords", help="Extra keywords to be processed by wordlist generator. Multiple keywords separated by comma (p.e. keyword1,keyword2,keyword3)")
    # Length (small, large, extralarge)

    other_group = parser.add_argument_group('Other options')
    other_group.add_argument("-d", "--debug", dest="debug", action="store_true", help="Print debug messages")
    other_group.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    return parser.parse_args()