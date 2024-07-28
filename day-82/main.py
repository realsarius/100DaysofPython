MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

user_input = input("Enter string: ")
user_input = user_input.upper()

user_morse_code = []
for index, char in enumerate(user_input):
    if user_input[index] != " ":
        if user_input[index] == "Ü":
            user_morse_code.append(MORSE_CODE_DICT["U"])
        elif user_input[index] == "İ":
            user_morse_code.append(MORSE_CODE_DICT["I"])
        elif user_input[index] == "Ö":
            user_morse_code.append(MORSE_CODE_DICT["O"])
        elif user_input[index] == "Ş":
            user_morse_code.append(MORSE_CODE_DICT["S"])
        elif user_input[index] == "Ğ":
            user_morse_code.append(MORSE_CODE_DICT["G"])
        elif user_input[index] == "Ç":
            user_morse_code.append(MORSE_CODE_DICT["C"])
        else:
            user_morse_code.append(MORSE_CODE_DICT[char])
    else:
        user_morse_code.append(" ")


user_morse_code = " ".join(user_morse_code)
print(user_morse_code)