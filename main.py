# for activate the venv
# source path/to/venv/bin/activate

# for run the code
# python3 -m main

from src.constants import *
from src.image_processing import Image_processing
from src.audio_processing import Audio_processing
from src.text_processing import Text_processing
from src.speech_recognition import Speech_recognition
from src.utils import *
import time

if __name__ == "__main__":
    print("* Set up *")
    # Create instance of each class.
    IMG_processor = Image_processing()
    AUDIO_processor = Audio_processing()
    TEXT_processor = Text_processing()
    SPEECH_processor = Speech_recognition()
    # testing image
    # preprocess
    # result = recognize_text(im_1_path)
    # img_1 = cv2.imread(im_1_path)
    # img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_1)
    # print(overlay_ocr_text(im_1_path, '1_carplate'))
    print("* Set up finished *")

    YES = [
        "ถูกต้อง",
        "ถูกต้องครับ",
        "ถูกต้องคับ",
        "ถูกต้องค่ะ",
        "ใช่",
        "ใช่ครับ",
        "ใช่คับ",
        "ใช่ค่ะ",
        "ใช่คะ",
        "ใช่จ้า",
        "ใช่ใช่",
    ]
    NO = [
        "ผิด",
        "ผิดค่ะ",
        "ผิดครับ",
        "ไม่ใช่",
        "ไม่",
        "ไม่ใช่ครับ",
        "ไม่ใช่คับ",
        "ไม่ครับ",
        "ไม่คับ",
        "ไม่ค่ะ",
        "ไม่คะ",
    ]
    glasses_user = False
    total_score = 0
    num_pic = 2
    total_pic = 0
    conclude_score = []
    result_global = ""
    change_page = True
    print("\nStart...")
    playsound_util(playsound_file_path["welcome"])
    time.sleep(1)

    print("* Check glasses for user *")
    while True:
        playsound_util(playsound_file_path["check_glasses"])
        res_rec = AUDIO_processor.record_audio()
        res_text = SPEECH_processor.get_text(res_rec)
        print("PURE_TEXT : %s" % (res_text))
        user_respond = TEXT_processor.process_user_respond(res_text)
        print("TRANSLATE_TO_RESPONSE : %s" % (user_respond))
        print("* User Response *")
        print("YES : %s" % (user_respond in YES))
        print("NO  : %s" % (user_respond in NO))
        if user_respond in YES:
            glasses_user = True
            print("USER : wear the glasses")
            break
        elif user_respond in NO:
            print("USER : don't wear the glasses")
            break
        else:
            print("Don't understand, please say it again.")
            playsound_util(playsound_file_path["cannot_catch"])

    time.sleep(1)

    for i in range(num_pic):
        print("\nWait for image processing....")
        playsound_util(playsound_file_path["process_pic"])

        # image processing
        # use for keep data from picture
        # result_append = IMG_processor.return_ocr_result()

        # for test only
        # fix data to check voice recon
        result_append = [
            ["6", "5"],
            ["2", "3", "9"],
        ]

        print("Finished image processing")
        print("\n* Test user's vision *")
        print(f"There are #{len(result_append)} lines ")
        print(f"All of numbers in this image are {result_append}")
        # if (change_page):
        print("\n* First line *")
        playsound_util(playsound_file_path["first_line"])
        # change_page=False
        count_line = 0
        total_pic += 1

        for i in result_append:

            # # old version
            # # print(i)
            # # playsound_util(playsound_file_path['initial'])
            # voice_recorded = AUDIO_processor.record_audio()
            # # playsound_util(playsound_file_path['got_your_voice'])
            # # audio_visualization(voice_recorded)
            # speech_text = SPEECH_processor.get_text(voice_recorded)
            # print("PURE_TEXT : %s" % (speech_text))
            # ref_text = TEXT_processor.process_digit_thai(i)
            # # print(speech_text)
            # hyp_text = TEXT_processor.process_text(speech_text)
            # print("TRANSLATE_TO_NUMBER : %s" % (hyp_text))

            # repeat_answer(hyp_text.split(" "))
            # correct_test = 0
            # # playsound_util(playsound_file_path['beep'])
            # count_line += 1
            # while hyp_text == "":
            #     voice_recorded = AUDIO_processor.record_audio()
            #     # playsound_util(playsound_file_path['got_your_voice'])
            #     # audio_visualization(voice_recorded)
            #     print("TEST SI")
            #     speech_text = SPEECH_processor.get_text(voice_recorded)

            #     ref_text = TEXT_processor.process_digit_thai(i)
            #     # print(speech_text)
            #     hyp_text = TEXT_processor.process_text(speech_text)

            #     repeat_answer(hyp_text.split(" "))

            # while True:
            #     # repeat_answer(hyp_text)
            #     res_rec = AUDIO_processor.record_audio()
            #     res_text = SPEECH_processor.get_text(res_rec)
            #     print(res_text)
            #     user_respond = TEXT_processor.process_user_respond(res_text)
            #     # debug
            #     print(user_respond)
            #     print(user_respond in YES, user_respond in NO)
            #     # playsound_util(playsound_file_path['beep'])

            #     if user_respond in YES:
            #         if count_line != len(result_append):
            #             # playsound_util(playsound_file_path['prepare'])
            #             playsound_util(playsound_file_path["next_line"])
            #             time.sleep(1)
            #         break

            #     elif user_respond in NO:
            #         playsound_util(playsound_file_path["repeat_same_line"])
            #         playsound_util(playsound_file_path["initial"])
            #         voice_recorded = AUDIO_processor.record_audio()
            #         # playsound_util(playsound_file_path['beep'])
            #         speech_text = SPEECH_processor.get_text(voice_recorded)
            #         hyp_text = TEXT_processor.process_text(speech_text)
            #         # playsound_util(playsound_file_path['got_your_voice'])
            #         repeat_answer(hyp_text.split(" "))

            #         while hyp_text == [""]:
            #             voice_recorded = AUDIO_processor.record_audio()
            #             # playsound_util(playsound_file_path['got_your_voice'])
            #             # audio_visualization(voice_recorded)
            #             speech_text = SPEECH_processor.get_text(voice_recorded)

            #             ref_text = TEXT_processor.process_digit_thai(i)
            #             # print(speech_text)
            #             hyp_text = TEXT_processor.process_text(speech_text)

            #             repeat_answer(hyp_text.split(" "))

            #     else:
            #         playsound_util(playsound_file_path["cannot_catch"])
            #         playsound_util(playsound_file_path["yes_or_no"])
            #         # playsound_util(playsound_file_path['beep'])

            # new version
            print(i)
            correct_test = 0
            count_line += 1
            while True:
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
                elif hyp_text != "":
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
                                AUDIO_processor,
                                SPEECH_processor,
                                TEXT_processor,
                                i,
                                YES,
                                NO,
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
                            res_rec = AUDIO_processor.record_audio()
                            res_text = SPEECH_processor.get_text(res_rec)
                            print("PURE_TEXT : %s" % (res_text))
                            user_respond = TEXT_processor.process_user_respond(res_text)
                            print("TRANSLATE_TO_RESPONSE : %s" % (user_respond))
                            print("* User Response *")
                            if user_respond in YES:
                                print("YES")
                                # all_num = len(i)
                                # current_num = len(hyp_text.split(" "))
                                # less_num = all_num - current_num
                                new_number = other_number(
                                    AUDIO_processor,
                                    SPEECH_processor,
                                    TEXT_processor,
                                    i,
                                    YES,
                                    NO,
                                )
                                hyp_text = hyp_text + " " + new_number
                                break

                            elif user_respond in NO:
                                print("NO")
                                break
                            else:
                                print("Don't understand, please say it again.")
                                playsound_util(playsound_file_path["cannot_catch"])

                        check_next_line(count_line, len(result_append), time)
                        break
                    else:
                        check_next_line(count_line, len(result_append), time)
                        break

            print(f"hyp_text: {hyp_text}")
            print(f"ref_text: {ref_text}")
            print("=========================================")
            evaluation_result = evaluation_score(
                ref_len=len(ref_text),
                hyp_len=len(hyp_text),
                hyp_text=hyp_text,
                ref_text=ref_text,
            )
            total_score += len(evaluation_result)
            resultg = result(len(i), correct_test)
            conclude_score.append((f"picture_number_{num_pic}", resultg))
            result_global = resultg
        if total_pic != num_pic:
            playsound_util(playsound_file_path["change_pic"])
        time.sleep(5)

    playsound_util(playsound_file_path["end_of_process"])
    print(f"Score: {total_score}")
    print(result_global)

    if result_global != "":
        line_no_and_with = extract_line_no(result_global)
        for i in str(line_no_and_with[0]):
            if i == "0":
                eye_sight = 200
            elif i == "1":
                eye_sight = 100
            elif i == "2":
                eye_sight = 70
            elif i == "3":
                eye_sight = 50
            elif i == "4":
                eye_sight = 40
            elif i == "5":
                eye_sight = 30
            elif i == "6":
                eye_sight = 25
            elif i == "7":
                eye_sight = 20
        eye_val = f"20/{eye_sight}"
        print(eye_val)

    # Example parameters for the visual acuity test result
    if glasses_user:
        write_va_result_to_file(
            re_sc="-",
            re_scph="-",
            re_cc=eye_val,
            re_ccph="-",
            le_sc="-",
            le_scph="-",
            le_cc=eye_val,
            le_ccph="-",
        )
    else:
        write_va_result_to_file(
            re_sc="eye_val",
            re_scph="-",
            re_cc="-",
            re_ccph="-",
            le_sc="eye_val",
            le_scph="-",
            le_cc="-",
            le_ccph="-",
        )
