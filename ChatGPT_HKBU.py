import configparser
import requests

import json
# 使用geopy库确定城市经纬度
from geopy.geocoders import Nominatim


def get_current_weather(location:str):

    # 创建地理编码器实例
    geolocator = Nominatim(user_agent="my_geocoder")

    # 获取城市经纬度
    city = location
    loca = geolocator.geocode(city)
    
    if loca:
        # 免费API，只能使用200次
        url = "https://eolink.o.apispace.com/456456/weather/v001/now"
        # 记得处理token
        headers = {
            "X-APISpace-Token":"sdasdasdasdasdasdasd"
        }
        payload = {"lonlat" : f"{loca.longitude},{loca.latitude}"}
        response=requests.request("GET", url, params=payload, headers=headers)
        response=response.json()
        
        weather_info = {
        "location": location,
        "weather": response["result"]["realtime"]["text"],
        "temperature": response["result"]["realtime"]["temp"],
        "time": response["result"]["last_update"],
        }
        
        return json.dumps(weather_info)
    
    else:
        # 未知地点
        return json.dumps({"location": location, "error": "Unknow location"})


class HKBU_ChatGPT():
    def __init__(self,config_='./config.ini'): 
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser: 
            self.config = config_

        # 保存对话历史
        self.conversation_history = []

    def submit(self, message):
        # 添加用户消息到历史记录
        self.conversation_history.append({"role": "user", "content": message})

        url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])

        headers = { 
            'Content-Type': 'application/json',
            'api-key': (self.config['CHATGPT']['ACCESS_TOKEN']) 
        } 
        
        # 使用完整对话历史
        payload = { 
            "messages": self.conversation_history,
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "获取指定位置的当前天气信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "城市名称，例如：北京、上海、香港"
                                }
                            },
                            "required": ["location"]
                        }
                    }
                }
            ],
            "tool_choice": "auto"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            
            data = response.json()
            assistant_message = data['choices'][0]['message']
            
            # 处理可能的函数调用
            if "tool_calls" in assistant_message:
                # 遍历所有工具调用
                for tool_call in assistant_message["tool_calls"]:
                    if tool_call["type"] == "function" and tool_call["function"]["name"] == "get_current_weather":
                        # 解析函数参数
                        function_args = json.loads(tool_call["function"]["arguments"])
                        location = function_args.get("location")
                        
                        # 调用天气函数
                        weather_result = get_current_weather(location)
                        
                        # 添加AI消息和工具调用结果到历史记录
                        self.conversation_history.append(assistant_message)
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": "get_current_weather",
                            "content": weather_result
                        })
                        
                        # 发送第二次请求以获取最终回复
                        second_response = requests.post(url, json={"messages": self.conversation_history}, headers=headers)
                        second_response.raise_for_status()
                        second_data = second_response.json()
                        final_message = second_data['choices'][0]['message']
                        
                        # 添加最终回复到历史记录
                        self.conversation_history.append(final_message)
                        return final_message["content"]
            else:
                # 没有工具调用，直接返回回复
                self.conversation_history.append(assistant_message)
                return assistant_message["content"]
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API error: {str(e)}"
            return error_msg
        except (KeyError, json.JSONDecodeError) as e:
            error_msg = f"Json paser error: {str(e)}"
            return error_msg

# class HKBU_ChatGPT():
#     def __init__(self,config_="./config.ini"):
#         if( type(config_)==str):
#             self.config=configparser.ConfigParser()
#             self.config.read(config_)
#         elif type(config_) == configparser.ConfigParser:
#             self.config = config_
    
#     def submit(self,message):
#         conversation=[
#             {
#                 "role": "user",
#                 "content": message
#             }
#         ]
#         url=(self.config["CHATGPT"]["BASICURL"])+\
#         "/deployments/"+(self.config["CHATGPT"]["MODELNAME"])+\
#         "/chat/completions/?api-version="+(self.config["CHATGPT"]["APIVERSION"])
        
#         headers = { 
#                 'Content-Type': 'application/json',
#                 'api-key': (self.config['CHATGPT']['ACCESS_TOKEN']) 
#             }
#         payload = { 'messages': conversation }
#         response = requests.post(url, json=payload, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             return data['choices'][0]['message']['content']
#         else:
#             return 'Error:', response
        
if __name__=="__main__":
    ChatGPT_test=HKBU_ChatGPT()
    
    while True:
        user_input=input("Typing anything to ChatGPT:\t")
        response = ChatGPT_test.submit(user_input)
        print(response)