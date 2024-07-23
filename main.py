# Running Part
# Step 1.
# Use for activating the venv
# source path/to/venv/bin/activate
# Step 2.
# Use for running the code
# python3 -m main

# Coding Part
# Import all necessary files
from src.constants import *
from src.image_processing import Image_processing
from src.audio_processing import Audio_processing
from src.text_processing import Text_processing
from src.speech_recognition import Speech_recognition
from src.utils import *
import time

# Start running
if __name__ == "__main__":
    # START "Set up system"
    print("* Set up *")
    # SUB_TASK "Create instance of each class."
    IMG_processor = Image_processing()
    SPEECH_processor = Speech_recognition()
    AUDIO_processor = Audio_processing(0, SPEECH_processor, "")
    TEXT_processor = Text_processing()

    # SUB_TASK "Test with image processing."
    # SUB_TASK "Preprocess"
    # result = recognize_text(im_1_path)
    # img_1 = cv2.imread(im_1_path)
    # img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_1)
    # print(overlay_ocr_text(im_1_path, '1_carplate'))

    print("* Set up finished *")
    # END "Set up system"

    # Set up necessary variables
    glasses_user = False
    total_score = 0
    num_pic = 2
    total_pic = 0
    conclude_score = []
    result_global = ""
    change_page = True
    user_continue = False
    correct_number = 0
    all_number = 0

    # Start testing
    print("\nStart...")
    # Welcome
    playsound_util(playsound_file_path["welcome"])
    time.sleep(1)

    # Check glasses for user
    print("* Check glasses for user *")
    glasses_user = check_glasses(AUDIO_processor, TEXT_processor)

    # START "Testing for all pictures"
    for i in range(num_pic):
        # START "Image Processing"
        print("\nWait for image processing....")
        playsound_util(playsound_file_path["process_pic"])

        # Use "Real Image Processing"
        result_append, scoring = IMG_processor.return_ocr_result()

        # Use "Mock Image Processing" (edit here for testing only voice)

        # result_append = [
        #     [8, 5],
        #     [2, 9, 3],
        #     [8, 7, 5, 4],
        #     [6, 3, 9, 5, 2],
        #     [4, 2, 8, 3, 5, 6],
        #     [3, 7, 4, 6, 2, 8, 5],
        #     [4, 2, 7, 5, 9, 3, 6],
        #     [7, 2, 6, 4, 7, 9, 3],
        #     [3, 8, 7, 5, 2, 6, 4],
        #     [6, 9, 3, 7, 4, 2, 5],
        # ]
        print("Finished image processing")
        # END "Image Processing"

        print("\n* Test user's vision *")
        print(f"There are #{len(result_append)} lines ")
        print("All of numbers in this image are :")
        for i in result_append:
            print(i)
        print("")
        print("\n* First line *")
        playsound_util(playsound_file_path["first_line"])
        count_line = 0
        total_pic += 1

        # START "Testing for all lines in that picture"
        for i in result_append:
            print(i)
            correct_test = 0
            count_line += 1
            ref_text = TEXT_processor.process_digit_thai(i)
            all_number += len(i)
            hyp_text = test_user(
                AUDIO_processor,
                TEXT_processor,
                SPEECH_processor,
                i,
            )

            # Show output for testing by a line
            print(f"hyp_text: {hyp_text}")
            print(f"ref_text: {ref_text}")

            print("\nCurrent Line : %d/%d\n" % (count_line, len(result_append)))

            check_number = count_same_elements(i, hyp_text.split(" "))
            print("* SCORE *")
            print("Line Score : %d/%d" % (check_number, len(i)))
            correct_number += check_number
            print("All Score : %d/%d" % (correct_number, all_number))
            print("=========================================")

            if check_number != len(i):
                user_continue = False
                diff = len(i) - check_number
                if diff == 1:
                    print("USER: Done, %d incorrect answer." % diff)
                else:
                    print("USER: Done, %d incorrect answers." % diff)
                break

            Result_Eyesight = calculate_score( correct_number, scoring)
            print("=========================================")
            print("Correct_number: ", correct_number)
            print("All_number: ", all_number)


        #     evaluation_result = evaluation_score(
        #         ref_len=len(ref_text),
        #         hyp_len=len(hyp_text),
        #         hyp_text=hyp_text,
        #         ref_text=ref_text,
        #     )

        #     check_next_line(count_line, len(result_append))

        #     total_score += len(evaluation_result)
        #     resultg = result(len(i), correct_test)
        #     conclude_score.append((f"picture_number_{num_pic}", resultg))
        #     result_global = resultg

        # # END "Testing for all lines in that picture"
        # if not (user_continue):
        #     break
        # # Change picture
        # if total_pic != num_pic:
        #     playsound_util(playsound_file_path["change_pic"])

    playsound_util(playsound_file_path["end_of_process"])
    # print(f"Score: {total_score}")
    # print(result_global)
    # END "Testing for all pictures"

    # def calculate_score(self, ref_text, correct_score, score_lines):
   
    # Result of testing
    # if result_global != "":
    #     line_no_and_with = extract_line_no(result_global)
    #     for i in str(line_no_and_with[0]):
    #         if i == "0":
    #             eye_sight = 200
    #         elif i == "1":
    #             eye_sight = 100
    #         elif i == "2":
    #             eye_sight = 70
    #         elif i == "3":
    #             eye_sight = 50
    #         elif i == "4":
    #             eye_sight = 40
    #         elif i == "5":
    #             eye_sight = 30
    #         elif i == "6":
    #             eye_sight = 25
    #         elif i == "7":
    #             eye_sight = 20
    
    eye_val = f"20/{Result_Eyesight}"
    print(eye_val)

    # Example parameters for the visual acuity test result
    if glasses_user:
        if eye_val != "":
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
        if eye_val != "":
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
