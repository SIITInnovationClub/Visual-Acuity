class Text_processing:
    def __init__(self):
        pass

    def process_text(self, text_sample: str) -> str:
        synonym_one = ["นึก", "นึ่ง", "นึง", "หนุ่ง", "อึ่ง"]
        synonym_two = ["ส่อง", "ซอง", "โฉง", "สอ"]
        synonym_three = ["ซ้ำ", "สาง", "สา"]
        synonym_four = ["สี", "ซี", "เส", "เส่", "สี่ย์", "สิ", "ซี่", "เศ่", "เส่ห์", "สื่", "สื่อ"]
        synonym_five = ["ฮา", "ฮ่า", "ห่า", "ฮ่ะ", "อ่า", "ฮะ", "ฮ้ะ", "ห้ะ", "ฮ้อ"]
        synonym_six = ["ฮก", "ฮ้ก", "ห้ก", "อก", "โหก", "หอก", "อก", "หบ"]
        synonym_seven = ["เจต", "เจ๋ด", "เจ้ด", "เก็ด"]
        synonym_eight = ["แปต", "แบ", "แป", "แตก", "แตด"]
        synonym_nine = ["เก่า", "ก้าว"]
        key = ["หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        key = (
            key
            + synonym_one
            + synonym_two
            + synonym_three
            + synonym_four
            + synonym_five
            + synonym_six
            + synonym_seven
            + synonym_eight
            + synonym_nine
        )
        result = []
        for i, word in enumerate(text_sample.split(" ")):
            if word in key:
                if word in synonym_one:
                    word = "หนึ่ง"
                elif word in synonym_two:
                    word = "สอง"
                elif word in synonym_three:
                    word = "สาม"
                elif word in synonym_four:
                    word = "สี่"
                elif word in synonym_five:
                    word = "ห้า"
                elif word in synonym_six:
                    word = "หก"
                elif word in synonym_seven:
                    word = "เจ็ด"
                elif word in synonym_eight:
                    word = "แปด"
                elif word in synonym_nine:
                    word = "เก้า"
                result.append(word)
        # result = ['หนึ่ง', 'สอง', 'สาม', 'สี่']
        hyp_text = ""
        for i, word in enumerate(result):
            if i < (len(result) - 1):
                hyp_text += word + " "
            else:
                hyp_text += word
        # print(f"ASR hypothesis: {hyp_text}")
        return hyp_text

    def process_user_respond(self, text_sample: str) -> str:
        # key = ['ใช่','ไม่']
        key = ["ถูกต้อง", "ผิด", "ครับ", "ค่ะ", "คะ", "คับ", "ใช่", "ไม่"]
        result = []
        for i, word in enumerate(text_sample.split(" ")):
            if word in key:
                result.append(word)
        # result = ['ใช่']
        # res_text = ""
        res_text = []
        for word in result:
            # if(i < (len(result) - 1)):
            #     res_text += word + " "
            # else:
            #     res_text += word
            res_text.append(word)
        # print(f"ASR hypothesis: {hyp_text}")
        return ("").join(res_text)

    # process digit to thai words
    def process_digit_thai(self, digits) -> str:
        digits = str(digits).strip()
        result_gathering = []
        digit_dict = {
            "1": "หนึ่ง",
            "2": "สอง",
            "3": "สาม",
            "4": "สี่",
            "5": "ห้า",
            "6": "หก",
            "7": "เจ็ด",
            "8": "แปด",
            "9": "เก้า",
        }
        for i_ in digits:
            result_gathering.append(digit_dict.get(i_, "0"))
        return " ".join(result_gathering)
