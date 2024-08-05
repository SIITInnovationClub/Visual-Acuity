import numpy as np  # type: ignore
import re
from src.constants import *
from datetime import datetime
from pydub import AudioSegment, effects  # type: ignore
from pydub.playback import play  # type: ignore
import pyaudio  # type: ignore
import time


def playsound_util(path):
    sound = AudioSegment.from_file(path)
    raw_data = sound.raw_data
    sample_width = sound.sample_width
    channels = sound.channels
    rate = sound.frame_rate

    # Define a callback function with chunk size
    def callback(in_data, frame_count, time_info, status):
        nonlocal raw_data
        num_bytes = frame_count * sample_width * channels
        if len(raw_data) > num_bytes:
            data_to_return = raw_data[:num_bytes]
            raw_data = raw_data[num_bytes:]
            return (data_to_return, pyaudio.paContinue)
        else:
            return (raw_data, pyaudio.paComplete)

    p = pyaudio.PyAudio()

    # Experiment with different chunk sizes (e.g., 1024, 2048)
    CHUNK_SIZE = 2048

    stream = p.open(
        format=p.get_format_from_width(sample_width),
        channels=channels,
        rate=rate,
        output=True,
        frames_per_buffer=CHUNK_SIZE,
        stream_callback=callback,
    )

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()


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
    AUDIO_processor,
    TEXT_processor,
    SPEECH_processor,
    i,
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
            print(f'{hyp_text.split(" ")}')

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

            break
    return hyp_text


def transform_nums_to_numbers(arr):
    word_to_number = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
    }
    return [word_to_number[word] for word in arr]


def transform_words_to_numbers(arr):
    word_to_number = {
        "หนึ่ง": 1,
        "สอง": 2,
        "สาม": 3,
        "สี่": 4,
        "ห้า": 5,
        "หก": 6,
        "เจ็ด": 7,
        "แปด": 8,
        "เก้า": 9,
    }
    return [word_to_number[word] for word in arr]


def transform_result_append(arr):
    big_result = []
    for i in arr:
        transform_result = transform_nums_to_numbers(i)
        big_result.append(transform_result)
    return big_result


def areEqual(arr1, arr2):
    print("Check answers")
    print("PURE: ", arr1, " ", arr2)

    N = len(arr1)
    M = len(arr2)

    if N != M:
        return False

    arr2 = transform_words_to_numbers(arr2)

    # Sort both arrays
    arr1.sort()
    arr2.sort()

    print("TRANSFORM: ", arr1, " ", arr2, "\n")

    for i in range(0, N):
        if arr1[i] != arr2[i]:
            return False

        return True


def count_same_elements(arr1, arr2):
    print("PURE: ", arr1, " ", arr2)
    N = len(arr1)
    M = len(arr2)

    arr2 = transform_words_to_numbers(arr2)

    if N != M:
        diff = N - M
        for i in range(diff):
            arr2.append(10)

    arr1.sort()
    arr2.sort()

    print("TRANSFORM: ", arr1, " ", arr2)
    same_count = 0

    i, j = 0, 0
    while i < N and j < M:
        if arr1[i] < arr2[j]:
            i += 1
        elif arr1[i] > arr2[j]:
            j += 1
        else:
            same_count += 1
            i += 1
            j += 1

    return same_count


# Reference Text: ['96824', '84846', '43242', '42633']
# correct_score = 14
# Scoring Index: 2
# Scoring Index Value: 40
# Your score will be 20/40


def calculate_score(
    correct_score, scoring, current_line, line_number, current_pic, past_last_line
):
    # Print the reference text for debugging
    # print("Reference Text:", ref_text)
    result_score = ""
    past = False
    # Calculate the index for scoring
    # num_lines = len(ref_text)  # Number of lines in ref_text

    if line_number == 1:
        scoring[0] = str(int(int(scoring[0]) / 2))
    if correct_score > 0:
        if current_line == 1:
            scoring_index = current_line
            result_score = f"{correct_score - line_number}"
        elif correct_score > line_number / 2:
            scoring_index = current_line
            result_score = f"{correct_score - line_number}"
        elif correct_score <= line_number / 2:
            if current_line != 0:
                scoring_index = current_line - 1
                result_score = f"+{correct_score}"
            else:
                scoring_index = 1
    else:
        if current_pic > 1:
            result = past_last_line
            past = True
        else:
            scoring_index = 1

    # Handle case where the scoring index is out of range
    if correct_score - line_number == 0:
        result_score = ""
    if not (past):
        result = scoring[int(scoring_index) - 1]
        print("Scoring Index:", scoring_index - 1)
    # Print results
    print("Scoring Index Value:", result)
    if line_number != 1:
        full_result = f"20/{result} " + result_score
    else:
        full_result = f"10/{result} " + result_score

    print(f"Your score will be {full_result}")

    return full_result


# Test the function
# ref_text = ['96824', '84846', '43242', '42633']
# correct_score = 15
# score_lines = [80,60,40,20]
# calculate_score(None, ref_text, correct_score, score_lines)
