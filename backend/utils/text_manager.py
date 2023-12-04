def replace_text_with_dict(text, replace_dict):
    for key in replace_dict:
        text = text.replace("{" + key + "}", replace_dict[key])
    return text