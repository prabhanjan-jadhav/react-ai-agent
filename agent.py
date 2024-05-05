from langchain_community.llms import HuggingFaceHub
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)
from langchain_community.chat_models.huggingface import ChatHuggingFace
import re, json
from prompts import *
from apis import *

API_TOKEN = "YOUR_HUGGINGFACE_API_TOKEN"

llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=API_TOKEN,
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 50,
        "temperature": 0.1,
        "repetition_penalty": 1.03,
    },
)
chat_model = ChatHuggingFace(llm=llm)

available_functions = ['getCurrentWeather', 'getLocation', 'getCurrentDatetime', 'translate2En', 'getLatestNews', 'searchWeb']

def perform_action(request):
    action = request.get("action")
    action_argument = request.get("action_argument")

    if action == "getLocation":
        return getLocation()
    elif action == "getCurrentWeather":
        return getCurrentWeather(action_argument)
    elif action == "getCurrentDatetime":
        return getCurrentDatetime()
    elif action == "translate2En":
        return translate2En(action_argument)
    elif action == "getLatestNews":
        return getLatestNews(action_argument)
    elif action == "searchWeb":
        return searchWeb(action_argument)
    else:
        return f"Unknown action or this action is not available: {action}. List of available actions: {available_functions}."

action_regex = re.compile(r'\nAction: (\w+): (.+?)\n', re.DOTALL)

def agent(query):
    messages = [
        SystemMessage(content=systemPrompt),
        HumanMessage(content=query),
    ]
    
    MAX_ITERATIONS = 6

    for i in range(MAX_ITERATIONS):
        print("ITER=", i+1)
        res = chat_model.invoke(messages)
        response_current = res.content.split('</s>')[2].split('|>')[1].split('PAUSE')[0].replace('\n\n', '\n').strip()
        match = action_regex.search(res.content.split('</s>')[2].split('|>')[1].split('PAUSE')[0])
        if match:
            action = match.group(1)
            action_argument = match.group(2)

            result_json = {"action": action, "action_argument": action_argument}

        else:
            if "Answer:" in res.content.split('</s>')[2].split('|>')[1].split('PAUSE')[0]:
                return res.content.split('</s>')[2].split('|>')[1].split('PAUSE')[0].split("Answer:")[-1]
                break
            else:
                print("No action found in the input string.")
        result = perform_action(result_json)

        updated_sys_prompt = res.content.split("</s>")[0]+res.content.split("</s>")[1]+res.content.split("</s>")[2].split("PAUSE")[0]+"\nPAUSE"
        messages = [
            SystemMessage(content=updated_sys_prompt),
            HumanMessage(content=f"\nObservation: {result}\n"),
        ]
    return res.content

output1 = agent("Question: What places can I visit today.")
print(output1)