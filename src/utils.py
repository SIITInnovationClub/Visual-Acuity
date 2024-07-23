import numpy as np  # type: ignore
import re
from src.constants import *
from datetime import datetime


def evaluation_score(ref_len, hyp_len, hyp_text, ref_text):
    checked_index = []
    correct = []
    if ref_len == hyp_len:
        print("ref_len == hyp_len")
        for i, hyp in enumerate(hyp_text.split(" ")):
            if hyp in ref_text.split(" "):
                print("true")
                correct.append(hyp)
            else:
                print(f"sub @ index {i} by {hyp}")

    elif ref_len < hyp_len:
        print("ref_len < hyp_len")
        for i, ref in enumerate(ref_text.split(" ")):
            for j, hyp in enumerate(hyp_text.split(" ")):
                if hyp in ref:
                    print(f"true {hyp}")
                    correct.append(hyp)
                    checked_index.append(j)
                    break
                elif (hyp not in ref) & (j >= i) & (j not in checked_index):
                    print(f"insert @ index {i} by {hyp}")

    # Unfinished for same number
    elif ref_len > hyp_len:
        print("ref_len > hyp_len")
        for i, ref in enumerate(ref_text.split(" ")):
            for j, hyp in enumerate(hyp_text.split(" ")):
                if hyp in ref:
                    print(f"true {hyp}")
                    correct.append(hyp)
                    checked_index.append(j)
                    break
                elif (hyp not in ref) & (j >= i) & (j not in checked_index):
                    print(f"Delete @ index {i} ")
    # print(expected == len(correct
    # print(expected, len(correct))
    print("=========================================")
    return correct


def check_score(n, score):
    if n > 3:
        limit = np.ceil(n / 2) - 1
    elif n == 3:
        limit = 1
    else:
        limit = 0

    if limit >= (n - score):
        if n == 8:
            return False, (n - score)
        else:
            return True, (n - score)
    else:
        return False, (n - score)


def result_score(n, incorrect, line=None):
    if line == None:
        line = n
    base_line = np.floor(n / 2)
    if incorrect > base_line:
        return (line - 1), (n - incorrect)
    else:
        return line, -incorrect


def end_line_txt(n):
    return n


def result(n, score, line=None):
    stop, incorrect = check_score(n, score)
    if stop == False:
        end_line, note = result_score(n, incorrect)
    end_line_text = f"End @ line {end_line} with {note}"
    return end_line_text


def repeat_answer(hyp_text):
    print(hyp_text, hyp_text != [""])
    if hyp_text != [""]:
        playsound_util(playsound_file_path["you_said"])
        for i in hyp_text:
            if len(i) == 1:
                new_i = [""]
                new_i.append(i)
                play_num_sound(new_i)
            else:
                play_num_sound(i)
        playsound_util(playsound_file_path["yes_or_no"])
    else:
        playsound_util(playsound_file_path["cannot_catch"])


def play_num_sound(num):
    try:
        playsound_util(playsound_file_path[f"{num}"])
    except:
        print("คุณไม่ได้พูดจ้า")


def extract_line_no(line):
    # Use regular expression to extract numbers
    numbers = re.findall(r"\d+", line)
    # Convert the extracted numbers to integers
    numbers = list(map(int, numbers))
    # Print the extracted numbers
    return numbers


def write_va_result_to_file(
    re_sc, re_scph, re_cc, re_ccph, le_sc, le_scph, le_cc, le_ccph
):
    # Get the current date and time
    current_datetime = datetime.now()
    date = current_datetime.strftime("%d/%m/%Y")
    time = current_datetime.strftime("%H:%M")

    modified_date = date.replace("/", "_")
    modified_time = time.replace(":", "_")

    # Create the content for the visual acuity test result
    content = (
        f"{date}\t{time}\n\n"
        "[ VA result ]\n\n"
        "At distance : 3 meter\n\n"
        "Right eye test\n"
        f"RE-sc :\t{re_sc}\n"
        f"RE-SCPH :\t{re_scph}\n"
        f"RE-CC :\t{re_cc}\n"
        f"RE-CCPH :\t{re_ccph}\n\n"
        "--------------------------\n\n"
        "At distance : 3 meter\n\n"
        "Left eye test\n"
        f"LE-sc :\t{le_sc}\n"
        f"LE-SCPH :\t{le_scph}\n"
        f"LE-CC :\t{le_cc}\n"
        f"LE-CCPH :\t{le_ccph}\n"
    )

    # Specify the file name: filename
    # Specify the file name
    filename = f"test_results/va_result_{modified_date}_{modified_time}.txt"

    # Write the content to the specified file
    with open(filename, "w") as file:
        file.write(content)

    print(f"Visual Acuity Test result written to {filename}")


def call_nurse():
    # Put call nurse function in here
    return


def repeat_test_user_vision(AUDIO_processor, SPEECH_processor, TEXT_processor, i):
    hyp_text = ""
    while hyp_text == "":
        playsound_util(playsound_file_path["repeat_same_line"])
        AUDIO_processor.arrayNum = len(i)
        AUDIO_processor.type = "number"
        # ref_text = TEXT_processor.process_digit_thai(i)
        hyp_text = AUDIO_processor.record_audio(TEXT_processor)

        # Not number
        if hyp_text == "":
            print("We can't translate it to number, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

    # Number
    if hyp_text != "":
        while True:
            repeat_answer(hyp_text.split(" "))
            AUDIO_processor.arrayNum = 1
            AUDIO_processor.type = "user"
            user_respond = AUDIO_processor.record_audio(TEXT_processor)
            print("User Response : %s" % user_respond)
            if user_respond == "YES":
                print("YES : Next step")
                break
            elif user_respond == "NO":
                print("NO : Go back")
                hyp_text = repeat_test_user_vision(
                    AUDIO_processor, SPEECH_processor, TEXT_processor, i
                )
                break
            else:
                print("Don't understand, please say it again.")
                playsound_util(playsound_file_path["cannot_catch"])
        return hyp_text


def other_number(AUDIO_processor, SPEECH_processor, TEXT_processor, i, arrayNum):
    hyp_text = ""
    while hyp_text == "":
        playsound_util(playsound_file_path["say_other_number"])
        AUDIO_processor.arrayNum = arrayNum
        AUDIO_processor.type = "number"
        # ref_text = TEXT_processor.process_digit_thai(i)
        hyp_text = AUDIO_processor.record_audio(TEXT_processor)

        # Not number
        if hyp_text == "":
            print("We can't translate it to number, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

    # Number
    if hyp_text != "":
        while True:
            repeat_answer(hyp_text.split(" "))
            AUDIO_processor.arrayNum = 1
            AUDIO_processor.type = "user"
            user_respond = AUDIO_processor.record_audio(TEXT_processor)
            print("User Response : %s" % user_respond)
            if user_respond == "YES":
                print("YES : Next step")
                break
            elif user_respond == "NO":
                print("NO : Go back")
                hyp_text = other_number(
                    AUDIO_processor,
                    SPEECH_processor,
                    TEXT_processor,
                    i,
                    len(i) - len(hyp_text),
                )
                break
            else:
                print("Don't understand, please say it again.")
                playsound_util(playsound_file_path["cannot_catch"])
        return hyp_text


def diff_length_array(input, check):
    l_input = len(input)
    l_check = len(check)
    if l_input < l_check:
        return True
    else:
        return False


def diff_two_array(input, check):
    l_input = len(input)
    l_check = len(check)
    if l_input == l_check:
        same_type_array = convert_string_to_number(input)
        if same_type_array == check:
            return False
        else:
            return True
    else:
        return True


def convert_string_to_number(array):
    new_array = []
    for i in array:
        match i:
            case "หนึ่ง":
                k = "1"
            case "สอง":
                k = "2"
            case "สาม":
                k = "3"
            case "สี่":
                k = "4"
            case "ห้า":
                k = "5"
            case "หก":
                k = "6"
            case "เจ็ด":
                k = "7"
            case "แปด":
                k = "8"
            case "เก้า":
                k = "9"
        new_array.append(k)
    print(f"{new_array}")
    return new_array


def check_next_line(current, all):
    if current != all:
        playsound_util(playsound_file_path["next_line"])


def check_glasses(AUDIO_processor, TEXT_processor):
    glasses_user = False
    while True:
        playsound_util(playsound_file_path["check_glasses"])
        AUDIO_processor.arrayNum = 1
        AUDIO_processor.type = "user"
        user_respond = AUDIO_processor.record_audio(TEXT_processor)
        print("User Response : %s" % user_respond)
        if user_respond == "YES":
            glasses_user = True
            print("USER : wear the glasses")
            break
        elif user_respond == "NO":
            print("USER : don't wear the glasses")
            break
        else:
            print("Don't understand, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])
    return glasses_user


def test_user(
    AUDIO_processor, TEXT_processor, SPEECH_processor, i, count_line, result_append
):
    hyp_text = ""
    while True:
        AUDIO_processor.arrayNum = len(i)
        AUDIO_processor.type = "number"
        hyp_text = AUDIO_processor.record_audio(TEXT_processor)

        # Not number
        if hyp_text == "":
            print("We can't translate it to number, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

        # Number
        elif hyp_text != "":
            while True:
                repeat_answer(hyp_text.split(" "))
                AUDIO_processor.arrayNum = 1
                AUDIO_processor.type = "user"
                user_respond = AUDIO_processor.record_audio(TEXT_processor)
                print("User Response : %s" % user_respond)
                if user_respond == "YES":
                    print("YES : Next step")
                    break
                elif user_respond == "NO":
                    print("NO : Go back")
                    hyp_text = repeat_test_user_vision(
                        AUDIO_processor,
                        SPEECH_processor,
                        TEXT_processor,
                        i,
                    )
                    break
                else:
                    print("Don't understand, please say it again.")
                    playsound_util(playsound_file_path["cannot_catch"])

            print(hyp_text)
            print(f"{hyp_text.split(" ")}")

            if diff_length_array(hyp_text.split(" "), i):
                while True:
                    playsound_util(playsound_file_path["check_other_number"])
                    AUDIO_processor.arrayNum = 1
                    AUDIO_processor.type = "user"
                    user_respond = AUDIO_processor.record_audio(TEXT_processor)
                    print("User Response : %s" % user_respond)
                    if user_respond == "YES":
                        new_number = other_number(
                            AUDIO_processor,
                            SPEECH_processor,
                            TEXT_processor,
                            i,
                            len(i) - len(hyp_text.split(" ")),
                        )
                        hyp_text = hyp_text + " " + new_number
                        break

                    elif user_respond == "NO":
                        break
                    else:
                        print("Don't understand, please say it again.")
                        playsound_util(playsound_file_path["cannot_catch"])

                check_next_line(count_line, len(result_append))
                break
            else:
                check_next_line(count_line, len(result_append))
                break
    return hyp_text

# Output:  ['6096824', '0084846', '443242', '3042633']
# Result should be

# Scoring Index / Scoring: ['20/60', '20/50', '20/40', '20/30']
# Final Output / Hyp_words : ['96824', '84846', '43242', '42633']

# If you say
# "9 6 8 2 4" , "8 4 8 4 6", "4 3 2 5 2" then you score will be 20/50 ..... 


def calculate_score(self, ref_text, hyp_text, score_lines):
        ref_lines = ref_text.split()
        hyp_words = hyp_text.split()

        scoring_index = []
        final_output = []
        total_correct = 0

        # Iterate over each line in the reference text
        for ref_word in ref_lines:
            # Extract digits only
            digits_only = "".join(filter(str.isdigit, ref_word))
            final_output.append(digits_only)

            # Calculate the corresponding visual acuity line
            length = len(digits_only)
            score = f"20/{length * 10}"
            scoring_index.append(score)

            # Calculate correct matches
            hyp_digits = "".join(filter(str.isdigit, hyp_words))
            correct_count = sum(1 for c in digits_only if c in hyp_digits)
            total_correct += correct_count

        # Determine final score using the provided score lines
        for score in score_lines:
            if total_correct >= len(hyp_words) * (1 - score / 100):  # adjust the threshold as needed
                final_score = f"20/{score}"
                break
        else:
            final_score = f"20/{score_lines[-1]}"  # default to the worst score if no match

        # Print results
        print("Scoring Index:", scoring_index)
        print("Final Output:", final_output)
        print(f"Your score will be {final_score}")

        return total_correct

