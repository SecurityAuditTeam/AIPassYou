import os
import json
from .data import Scan
from openai import OpenAI

def search(scan: Scan, model: str = 'gpt-3.5-turbo', temperature: float = 0.5, nkw: int = 5):
    base = query(prompt_base(scan, nkw), model, temperature)
    base['extended'] = query(prompt_ext(base, nkw), model, temperature)
    base['passwords2'] = query(prompt_pwds(base, 100), model, temperature)
    return base

def query(prompt, model, temperature):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key = api_key)

    response = client.chat.completions.create(
        model = model,
        temperature = temperature,
        response_format = {"type": "json_object"},
        messages = prompt
    )

    finish_reason = response.choices[0].finish_reason

    if (finish_reason == "stop"):
        data = response.choices[0].message.content
        json_response = json.loads(data)
        return json_response
    else:
        print("Error! provide more tokens please")
        exit(0)

def prompt_base(scan: Scan, nkeywords: int = 5):
    return [{
            "role": "system",
            "content": f"You are a helpful AI assistant and expert in data analisys. The user will provide you information from their social networks and I will ask you for information about it. The input will be provided using a JSON schema defined as: {Scan.model_json_schema()}."
        }, {
            "role": "assistant", 
            "content": "Below you will find the user information:"
        }, {  
            "role": "assistant", 
            "content": scan.model_dump_json(exclude_none=True)
        }, {
            "role": "user", 
            "content": 
                "I need you to answer me some questions related to the information I gave you. "+ 
                "Please answer each question in a single line, as a json array of keywords, and do not include any other text or symbol.\n"+
                "I expect you to reply using the same language used in the provided information.\n" +
                "The questions are: \n"+
                f"[name]: Can you provide {nkeywords} possible results on what can be the user full name?\n"+
                f"[location]: Can you provide {nkeywords} possible locations that can be related in any way to the user?\n"+
                f"[hobbies]: Can you provide {nkeywords} possible user hobbies?\n"+
                f"[general]: Can you provide {nkeywords} keywords that define the user?\n"+
                f"[posts]: Can you provide {nkeywords} keywords from user publications?\n"+
                f"[birth]: Can you provide {nkeywords} possible birth years?\n"+
                f"[age]: Can you provide {nkeywords} possible results for user age?\n"+
                f"[username]: Can you provide {nkeywords} possible social network usernames that can be used by the user?\n"+
                f"[pettype]: Can you provide {nkeywords} possible pet types that user loves (in user's language)?\n"+
                f"[petname]: Can you provide {nkeywords} possible pet names?\n"+
                f"[familynames]: Can you provide {nkeywords} family member names, for people such as children, parents or similar?\n"+
                f"[familybirthyears]: Can you provide {nkeywords} possible bith years from that family members?\n"+
                f"[languages]: Can you provide {nkeywords} possible languages it is using? If you do not know any, use 'user' keyword\n"+
                f"[jobs]: Can you provide {nkeywords} possible user jobs?\n"+
                f"[companies]: Can you provide {nkeywords} possible companies where the user works or has worked?\n"+
                f"[passwords]: Can you provide 50 possible passwords the user can use?\n"
        }]

def prompt_ext(base: dict, nkeywords: int = 5):
    # numeros o años | sort uniq -> cosas relevantes de esos años y de la decada y de el milenio
    # localidades -> info de las localidades
    # posts y hobbies
    # jobs or company
    
    return [
        {
            "role": "system",
            "content": f"You are a helpful AI assistant expert in events and world locations. It is REALLY IMPORTANT that you answer me using {base['languages'][0]} language. The output will be formatted in JSON."
        }, {
            "role": "user", 
            "content": 
                "I have some questions for you. Please answer each question in a single line, as a JSON array of keywords, and do not include any other text or symbol. \n"+
                "The questions are: \n"+
                f"[locations]: Can you provide {nkeywords} keywords for each one of the following cities or countries: {','.join(base['location'])}?\n" +
                f"[years]: Can you provide {nkeywords} keywords for interesting events occured in each one of these years: {','.join(base['birth'])}?\n" +
                f"[years_hobbies]: Can you provide {nkeywords} keywords for interesting events related to these topics ({','.join(base['hobbies'])}) that occured in each one of these years: {','.join(base['birth'])}?\n" +
                f"[jobs]: Can you provide {nkeywords} keywords for each one of the following jobs: {','.join(base['jobs'])}?\n" +
                f"[companies]: Can you provide {nkeywords} keywords for each one of the following companies: {','.join(base['companies'])}?\n" 
                f"[hobbies]: Can you provide {nkeywords} keywords for each one of the following hobbies: {','.join(base['hobbies'])}?\n" +
                f"[hobbies_location]: Can you provide {nkeywords} keywords for each of the following hobbies ({','.join(base['hobbies'])}) in the contexto of these locations ({','.join(base['location'])})?\n" +
                f"[posts]: Can you provide {nkeywords} keywords for each one of the following topics: {','.join(base['hobbies'])}?" 
    }]

def prompt_pwds(base, nkeywords: int = 5):
    return [
        {
            "role": "system",
            "content": f"You are a helpful AI assistant and expert in data analisys. The user will provide you a JSON including a list if keywords and you are expected to response with {nkeywords}  passwords derivated from that information with a minimum length of 6 characters and a maximum length of 15 characters in JSON format."
        },
        {
            "role": "user", 
            "content": json.dumps(base)
        }
    ]