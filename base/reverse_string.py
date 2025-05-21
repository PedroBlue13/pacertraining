def inverse(text):
    return text[::-1]

try:
    input_text = input("Type a word or phrase to invert: \n")
    
    if not input_text.strip():
        raise ValueError("You need to type somethin!")
    result = inverse(input_text)
    print(f"Inverted text:\n{result}")
except Exception as e:
    print(f"have anything error: {e}" )