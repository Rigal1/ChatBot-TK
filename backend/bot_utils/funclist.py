def reply_message():
    functions = [
            {
                "type": "function",
                "function": {
                    "name": "reply_message",
                    "description": "Get replies and information from chatbot",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "emotion": {
                                "type": "string",
                                # "enum": ["NEUTRAL", "JOY", "ANGRY", "SAD", "CONFUSION", "SURPRISED", "LOVE", "BLUSHING"],
                                # "enum": ["NEUTRAL", "JOY", "ANGRY", "SAD", "CONFUSION", "SURPRISED"],
                                # "enum": ["NEUTRAL", "KINDNESS", "ANGRY", "SAD", "CONFUSION"],
                                "enum": ["NEUTRAL", "JOY", "ANGRY", "SAD", "CONFUSION", "SURPRISED", "LOVE", "HORNY"],
                                "description": "The most suitable emotion for the chatbot"
                            },
                            "reply": {
                                "type": "string",
                                "description": "The content that the chatbot responds to after receiving input. The contents of \"CharacterProfile\" must be strictly followed."
                            }
                        },
                        "required": ["emotion", "reply"]
                    }
                }
            }
        ]
    return functions

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

def estimate_emotion():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "estimate_emotion",
                "description": "Estimate the emotion of the chatbot",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "emotion": {
                            "type": "string",
                            "enum": ["neutral", "kindness", "joy", "angry", "sad", "confusion", "surprised", "love", "blushing", "horny"],
                            "description": "The most suitable emotion for the chatbot"
                        },
                    },
                    "required": ["emotion"],
                },
            },
        }
    ]
    return tools
