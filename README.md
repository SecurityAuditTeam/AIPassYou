# AIPassYou (AI.PY)

<img src="https://github.com/SecurityAuditTeam/AIPassYou/blob/main/logo.png?raw=true" height="256" width="256">

# Summary

The tool allows you to generate a dictionary of passwords based on data extracted from your social networks, including personalized information about hobbies, geographic location or language.

The process is divided into three points:

* Extraction of information from social networks
* Use of AI to find keywords inferred from this public information.
* Rule-based dictionary generation process

This process allows the generation of customized dictionaries that greatly increase the effectiveness over traditional password dictionaries.

## Key features

- Personal keywords
- User language sensitive
- Geographic location based keywords

## Installation

To run the latest version of the code, you can install it from Git:

```bash
$ git clone https://github.com/SecurityAuditTeam/AIPassYou.git
$ cd AIPassYou
$ pip install -r requirements.txt
```
Make sure you have installed **Python 3.6+** and **pip3** in your environment

## Configuration

The program needs some credentials to be configured before it can be run. Those credentials can be configured in the **.env** file that can be copied from **.env.example**:

```bash
$ cp .env.example .env
```

The most important parameter to be configured is the **ChatGPT API Key**, that it's the only required parameter. The other ones are related to social network credentials and are only required if you want to access private profiles or some extra information:

## Usage

```bash
$ python3 mAIprogram.py -h
usage: mAIprogram [-i INSTAGRAM] [-t TWITTER] [-f FACEBOOK] [-l LINKEDIN] [--num-posts NPOST] [--temperature TEMPERATURE] [--model MODEL]
                  [--num-keywords NKEYWORDS] [-o OUTPUT] [--save-data SDATA] [--load-data LDATA] [--save-keywords SKEYWORDS] [-k KEYWORDS] [-d] [-h]

Social network options:
  -i INSTAGRAM, --instagram INSTAGRAM
                        Instagram username
  -t TWITTER, --twitter TWITTER
                        Twitter username
  -f FACEBOOK, --facebook FACEBOOK
                        Facebook username
  -l LINKEDIN, --linkedin LINKEDIN
                        LinkedIn username
  --num-posts NPOST     Number of posts to load from Social Networks (default: 20)

ChatGPT options:
  --temperature TEMPERATURE
                        ChatGPT temperature (default: '0.5')
  --model MODEL         ChatGPT model (default: 'gpt-3.5-turbo')
  --num-keywords NKEYWORDS
                        Number of keywords for each question (default: 5)

Input/output options:
  -o OUTPUT, --output OUTPUT
                        Wordlist output file (default to stdout)
  --save-data SDATA     Save social networks information to JSON file
  --load-data LDATA     Load social networks information from JSON file
  --save-keywords SKEYWORDS
                        Save AI generated keywords to JSON file

Wordlist options:
  -k KEYWORDS, --keywords KEYWORDS
                        Extra keywords to be processed by wordlist generator. Multiple keywords separated by comma (p.e. keyword1,keyword2,keyword3)

Other options:
  -d, --debug           Print debug messages
  -h, --help            show this help message and exit
```

## Examples

Basic usage using Twitter and Instagram social networks and writting wordlist into a file instead of stdout:

```
python3 AIPassYou.py -t <twitter_username> -i <instagram_username> -o wordlist.txt
```

You can save intermediate information to avoid retrieving the same information while testing:

```
$ python3 AIPassYou.py -t <twitter_username> -i <instagram_username> --save-data data.json --save-keywords keywords.json
[*] Loading information from Twitter profile '<twitter_username>'...  Done!
[*] Loading information from Instagram profile '<instagram_username>'...  Done!
pajaro
pajaro!
pajaro@
pajaro$
pajaro%
pajaro.
pajaro1
...
```

Then it can be loaded from those files. If you want to generate new keywords from chatGPT you can use:

```
$ python3 AIPassYou.py --load-data data.json 
...
B00ks1960
B00ks1960!
B00ks1960@
B00ks1960$
B00ks1960%
B00ks1960.
tastings
tastings!
tastings@
tastings$
tastings%
tastings.
...
```

Or re-generate a wordlist from extracted keywords:

```
$ python3 AIPassYou.py --load-keywords keywords.json 
```

## Results

The user profile is properly filled most of the time, getting intermitent errors from chatGPT response. 

For wordlist generation, it is using basic permutation rules, that generates dictionaries **from 1M to 10M** possible passwords.

It was tested against other well-known password dictionaries, such as rockyou.txt, by selecting some accounts disclosed in public breaches. The tools was executed against its social networks and checked if the password disclosed was included in the generated wordlist, obtaining the following results:

- The password was correctly guessed for **40% of the accounts**.
- The traditional wordlists had a success rate of 10% using same accounts.
- According to known password formats it was checked that the use of more advanced permutation rules, could increase rating to 62%.
- Same permutation rules using rockyou.txt, will achieve 30% but requiring 10x times more words.

## ToDo

- Add support for other social networks like linkedin
- Improve support and extracted data from facebook and instagram
- AI fine tunning to avoid empty sections 
- AI: Compatibility with ollama 
- Wordlist generator complexity
- Error handling


## Authors

* Marc Ulldemolins [(LinkedIn)](https://www.linkedin.com/in/marc-ulldemolins-9b2006209/)
* Maria Jesús Prior [(LinkedIn)](https://www.linkedin.com/in/maria-jesús-prior-bruno-848a87204/)
* Manuel Ginés [(LinkedIn)](https://www.linkedin.com/in/manuelgines/)
