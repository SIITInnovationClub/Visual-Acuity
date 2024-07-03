import numpy as np
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
    # key = ['หนึ่ง','สอง','สาม','สี่','ห้า','หก','เจ็ด','แปด','เก้า']
    # if num == key[0]:
    #     playsound_util(playsound_file_path['หนึ่ง'])
    #
    # elif num == key[1]:
    #     playsound_util(playsound_file_path['สอง'])
    #
    # elif num == key[2]:
    #     playsound_util(playsound_file_path['สาม'])
    #
    # elif num == key[3]:
    #     playsound_util(playsound_file_path['สี่'])
    #
    # elif num == key[4]:
    #     playsound_util(playsound_file_path['ห้า'])
    #
    # elif num == key[5]:
    #     playsound_util(playsound_file_path['หก'])
    #
    # elif num == key[6]:
    #     playsound_util(playsound_file_path['เจ็ด'])
    #
    # elif num == key[7]:
    #     playsound_util(playsound_file_path['แปด'])
    #
    # elif num == key[8]:
    #     playsound_util(playsound_file_path['เก้า'])


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


def repeat_test_user_vision(
    AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
):
    hyp_text = ""
    while hyp_text == "":
        playsound_util(playsound_file_path["repeat_same_line"])
        voice_recorded = AUDIO_processor.record_audio()
        speech_text = SPEECH_processor.get_text(voice_recorded)
        print("PURE_TEXT : %s" % (speech_text))
        ref_text = TEXT_processor.process_digit_thai(i)
        hyp_text = TEXT_processor.process_text(speech_text)
        print("TRANSLATE_TO_NUMBER : %s" % (hyp_text))

        # Not number
        if hyp_text == "":
            print("We can't translate it to number, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

    # Number
    if hyp_text != "":
        while True:
            repeat_answer(hyp_text.split(" "))
            res_rec = AUDIO_processor.record_audio()
            res_text = SPEECH_processor.get_text(res_rec)
            print(res_text)
            user_respond = TEXT_processor.process_user_respond(res_text)
            print(user_respond)
            print(user_respond in YES, user_respond in NO)
            if user_respond in YES:
                print("YES : Next step")
                break
            elif user_respond in NO:
                print("NO : Go back")
                hyp_text = repeat_test_user_vision(
                    AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
                )
                break
            else:
                print("Don't understand, please say it again.")
                playsound_util(playsound_file_path["cannot_catch"])
        return hyp_text


def other_number(AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO):
    hyp_text = ""
    while hyp_text == "":
        playsound_util(playsound_file_path["say_other_number"])
        voice_recorded = AUDIO_processor.record_audio()
        speech_text = SPEECH_processor.get_text(voice_recorded)
        print("PURE_TEXT : %s" % (speech_text))
        ref_text = TEXT_processor.process_digit_thai(i)
        hyp_text = TEXT_processor.process_text(speech_text)
        print("TRANSLATE_TO_NUMBER : %s" % (hyp_text))

        # Not number
        if hyp_text == "":
            print("We can't translate it to number, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

    # Number
    if hyp_text != "":
        while True:
            repeat_answer(hyp_text.split(" "))
            res_rec = AUDIO_processor.record_audio()
            res_text = SPEECH_processor.get_text(res_rec)
            print(res_text)
            user_respond = TEXT_processor.process_user_respond(res_text)
            print(user_respond)
            print(user_respond in YES, user_respond in NO)
            if user_respond in YES:
                print("YES : Next step")
                break
            elif user_respond in NO:
                print("NO : Go back")
                hyp_text = other_number(
                    AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
                )
                break
            else:
                print("Don't understand, please say it again.")
                playsound_util(playsound_file_path["cannot_catch"])
        return hyp_text


# def repeat_test_user_vision_2(
#     AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
# ):
#     hyp_text = ""
#     while hyp_text == "":
#         playsound_util(playsound_file_path["repeat_same_line"])
#         voice_recorded = AUDIO_processor.record_audio()
#         speech_text = SPEECH_processor.get_text(voice_recorded)
#         print("PURE_TEXT : %s" % (speech_text))
#         ref_text = TEXT_processor.process_digit_thai(i)
#         hyp_text = TEXT_processor.process_text(speech_text)
#         print("TRANSLATE_TO_NUMBER : %s" % (hyp_text))

#         # Not number
#         if hyp_text == "":
#             print("We can't translate it to number, please say it again.")
#             playsound_util(playsound_file_path["cannot_catch"])

#     # Number
#     if hyp_text != "":
#         while True:
#             repeat_answer(hyp_text.split(" "))
#             res_rec = AUDIO_processor.record_audio()
#             res_text = SPEECH_processor.get_text(res_rec)
#             print(res_text)
#             user_respond = TEXT_processor.process_user_respond(res_text)
#             print(user_respond)
#             print(user_respond in YES, user_respond in NO)
#             if user_respond in YES:
#                 print("YES : Next step")
#                 break
#             elif user_respond in NO:
#                 print("NO : Go back")
#                 hyp_text = repeat_test_user_vision(
#                     AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
#                 )
#                 break
#             else:
#                 print("Don't understand, please say it again.")
#                 playsound_util(playsound_file_path["cannot_catch"])

#         print(hyp_text)
#         print(f"{hyp_text.split(" ")}")
#         if diff_two_array(hyp_text.split(" "), i):
#             while True:
#                 playsound_util(playsound_file_path["check_number"])
#                 res_rec = AUDIO_processor.record_audio()
#                 res_text = SPEECH_processor.get_text(res_rec)
#                 print("PURE_TEXT : %s" % (res_text))
#                 user_respond = TEXT_processor.process_user_respond(res_text)
#                 print("TRANSLATE_TO_RESPONSE : %s" % (user_respond))
#                 print("* User Response *")
#                 if user_respond in YES:
#                     print("YES")
#                     user_result = False
#                     break
#                 elif user_respond in NO:
#                     user_result = repeat_test_user_vision_2(
#                         AUDIO_processor, SPEECH_processor, TEXT_processor, i, YES, NO
#                     )
#                     break
#                 else:
#                     print("Don't understand, please say it again.")
#                     playsound_util(playsound_file_path["cannot_catch"])
#             return user_result

#         else:
#             print("Test correct")
#             user_result = True
#             return user_result


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


def check_next_line(current, all, time):
    if current != all:
        playsound_util(playsound_file_path["next_line"])
        time.sleep(2)
