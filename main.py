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
    # Set up system
    print("* Set up *")
    # Create instance of each class.
    IMG_processor = Image_processing()
    SPEECH_processor = Speech_recognition()
    AUDIO_processor = Audio_processing(0, SPEECH_processor, "")
    TEXT_processor = Text_processing()
    # testing image
    # preprocess
    # result = recognize_text(im_1_path)
    # img_1 = cv2.imread(im_1_path)
    # img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    # plt.imshow(img_1)
    # print(overlay_ocr_text(im_1_path, '1_carplate'))
    print("* Set up finished *")

    # Set up variables
    glasses_user = False
    total_score = 0
    num_pic = 2
    total_pic = 0
    conclude_score = []
    result_global = ""
    change_page = True

    # Start
    print("\nStart...")
    playsound_util(playsound_file_path["welcome"])
    time.sleep(1)

    # Check glasses
    print("* Check glasses for user *")
    glasses_user = check_glasses(AUDIO_processor, TEXT_processor)
    time.sleep(1)

    # Loop by number of pictures
    for i in range(num_pic):
        # Image processing
        print("\nWait for image processing....")
        playsound_util(playsound_file_path["process_pic"])

        # use for keep data from picture
        # result_append ,scoring = IMG_processor.return_ocr_result()

        # for test only
        # fix data to check voice recon
        result_append = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
            ["9", "8", "7", "6", "5", "4", "3", "2", "1"],
            ["6", "5"],
            ["2", "3", "9"],
        ]
        print("Finished image processing")

        # testing
        print("\n* Test user's vision *")
        print(f"There are #{len(result_append)} lines ")
        print(f"All of numbers in this image are {result_append}")
        # if (change_page):
        print("\n* First line *")
        playsound_util(playsound_file_path["first_line"])
        # change_page=False
        count_line = 0
        total_pic += 1

        # loop by lines in picture
        for i in result_append:

            # start testing line
            print(i)
            correct_test = 0
            count_line += 1
            ref_text = TEXT_processor.process_digit_thai(i)
            hyp_text = test_user(
                AUDIO_processor,
                TEXT_processor,
                SPEECH_processor,
                i,
                count_line,
                result_append,
            )
            # end testing line

            # output
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

        # change picture
        if total_pic != num_pic:
            playsound_util(playsound_file_path["change_pic"])

    # end testing picture
    playsound_util(playsound_file_path["end_of_process"])
    print(f"Score: {total_score}")
    print(result_global)

    # result
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
