from playsound import playsound  # type: ignore


def playsound_util(path):
    playsound(path)


# FILE PATH
playsound_file_path = {
    "หนึ่ง": ("soundtrack/หนึ่ง.wav"),
    "สอง": "soundtrack/สอง.wav",
    "สาม": "soundtrack/สาม.wav",
    "สี่": "soundtrack/สี่.wav",
    "ห้า": "soundtrack/ห้า.wav",
    "หก": "soundtrack/หก.wav",
    "เจ็ด": "soundtrack/เจ็ด.wav",
    "แปด": "soundtrack/แปด.wav",
    "เก้า": "soundtrack/เก้า.wav",
    "beep": "soundtrack/X2Download.app - Censor beep sound effect (128 kbps).wav",
    "prepare": "soundtrack/เตรียมตัวพูดบรรทัดใหม่หล.wav",
    "repeat_same_line": "soundtrack/เริ่มการอัดเสียงในบรรทัด.wav",
    "initial": "soundtrack/พูดหลังเสียงสัญญาณได้เลย.wav",
    "yes_or_no": "soundtrack/ใช่หรือไม่.wav",
    "cannot_catch": "soundtrack/เราได้ยินคุณไม่ชัดกรุณาพ.wav",
    "got_your_voice": "soundtrack/ได้รับข้อมูลเสียงแล้วค่ะ.wav",
    "you_said": "soundtrack/คุณพูด.wav",
    "end_of_process": "soundtrack/สิ้นสุดกระบวนการวัดค่าสา.wav",
    "process_pic": "soundtrack/Process pic.wav",
    "change_pic": "soundtrack/Change pic.wav",
    "welcome": "soundtrack/สวัสดีค่ะคุณกำลังเข้าสู่.wav",
    "first_line": "soundtrack/เริ่มพูดบรรทัดแรกได้เลยค.wav",
    "next_line": "soundtrack/เริ่มพูดบรรทัดถัดไปได้เล.wav",
    "check_number": "soundtrack/เลขที่คุณเห็น.wav",
    "check_glasses": "soundtrack/คุณใส่แว่นสายตาใช่หรือไม่.wav",
    "call_nurse": "soundtrack/กำลังเรียกพยาบาล.wav",
    "nurse": "soundtrack/พยาบาลกำลังมา.wav",
    "check_other_number": "soundtrack/คุณเห็นเลขอื่นอีกใช่หรือไม่.wav",
    "say_other_number": "soundtrack/พูดเลขที่คุณเห็นเพิ่มหลังเสียงสัญญาณ.wav",
}


# SYNONYM
synonym = {
    # NUMBER
    "one": ["นึก", "นึ่ง", "นึง", "หนุ่ง", "อึ่ง"],
    "two": ["ส่อง", "ซอง", "โฉง", "สอ"],
    "three": ["ซ้ำ", "สาง", "สา"],
    "four": ["สี", "ซี", "เส", "เส่", "สี่ย์", "สิ", "ซี่", "เศ่", "เส่ห์", "สื่", "สื่อ", "สิ่"],
    "five": ["ฮา", "ฮ่า", "ห่า", "ฮ่ะ", "อ่า", "ฮะ", "ฮ้ะ", "ห้ะ", "ฮ้อ", "หาก", "ห้อ", "ถ้า"],
    "six": ["ฮก", "ฮ้ก", "ห้ก", "อก", "โหก", "หอก", "อก", "หบ", "โอก", "ปก", "นก"],
    "seven": ["เจต", "เจ๋ด", "เจ้ด", "เก็ด"],
    "eight": ["แปต", "แบ", "แป", "แตก", "แตด"],
    "nine": ["เก่า", "ก้าว", "เก้"],
    # RESPONSE
    "yes": [
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
        "ช่าย",
        "ชั่ย",
        "ช่าย",
        "ช่า",
        "ช่",
        "ใช้",
        "ใช่",
        "ใช",
        "แช็ก",
    ],
    "no": [
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
        "ไหม้",
        "ไม่ไม่",
    ],
}
