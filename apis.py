import requests, uuid

def getLocation(ip_address=''):
    base_url = f"http://ipinfo.io/{ip_address}/json"
    
    try:
        response = requests.get(base_url)
        data = response.json()

        if response.status_code == 200:
            return f"Location: {data['city']}, {data['region']}, {data['country']}"
        else:
            print(f"Error: {data['error']}. The input to this api is invalid either you're using .")
            pass

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def getCurrentWeather(action_argument):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': action_argument,
        'appid': 'YOUR_OPENWEATHERMAP_API_KEY',
        'units': 'metric' 
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            answer = f"Temperature in {action_argument}: {data['main']['temp']}°C" + "\n" + f"Weather: {data['weather'][0]['description']}"
            return answer
        else:
            pass
            # return f"Error: {data['message']}"
            # print(f"Error: {data['message']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def getCurrentDatetime():
    api_url = "http://worldtimeapi.org/api/ip"

    try:
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            current_datetime = data['utc_datetime'][:19]
            return f"Date: {current_datetime.split('T')[0]} Time: {current_datetime.split('T')[1]}"
        else:
            pass
            # return f"Error: {data['error']}"

    except Exception as e:
        pass
        # return f"An error occurred: {e}"

def translate2En(request_data):
    key = "YOUR_AZURE_TRANSLATOR_KEY"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path
    location = "southeastasia"

    try:
        text = request_data
        target_lang = 'en'

        params = {'api-version': '3.0', 'to': target_lang}

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        body = [{'text': text}]
        
        response = requests.post(constructed_url, params=params, headers=headers, json=body)
        response_data = response.json()

        if response.status_code == 200:
            return response_data[0]['translations'][0]['text']
        else:
            # pass
            return f"Error: {response_data['error']['message']}"

    except Exception as e:
        # pass
        return f"An error occurred: {e}"
    
def getLatestNews(country='us'):
    api_url = f"https://newsapi.org/v2/top-headlines"
    
    params = {
        'country': country,
        'apiKey': 'YOUR_NEWSAPI_KEY'
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        if response.status_code == 200:
            articles = data['articles'][:5]
            latest_news = ""
            for idx, article in enumerate(articles, start=1):
                latest_news+=f"News {idx}: {article['title']}"+"\n"
            return latest_news
        else:
            return f"Error: {data['message']}"

    except Exception as e:
        return f"An error occurred: {e}"

def searchWeb(query, count=5):
    base_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {
        "Ocp-Apim-Subscription-Key": 'YOUR_BING_SEARCH_API_KEY',
    }

    params = {
        "q": query,
        "count": count,
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200:
            results = data.get('webPages', {}).get('value', [])
            ret = "Search Results:\n"
            for idx, result in enumerate(results, start=1):
                ret += f"{idx}. "
                if 'snippet' in result:
                    ret += f"{result['snippet']}\n"
            return ret
        else:
            return f"Error: {data['error']['message']}"

    except Exception as e:
        return f"An error occurred: {e}"
