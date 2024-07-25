import easyocr  # type: ignore
import cv2  # type: ignore


class Image_processing:

    def __init__(self):
        self.repeat_count = 0

    def pre_process(self):
        pass

    def split_digits(self, ocr_result):
        """Split OCR results into single digits."""
        bbox, number, _ = ocr_result
        return [(bbox, digit) for digit in number if digit.isdigit()]

    def is_on_same_line(self, bbox1, bbox2, threshold=40):
        """Check if two bounding boxes are on the same line."""
        y1_center = (bbox1[0][1] + bbox1[2][1]) / 2
        y2_center = (bbox2[0][1] + bbox2[2][1]) / 2
        return abs(y1_center - y2_center) <= threshold

    def process_ocr_results(self, ocr_results, previous_texts, repeat_threshold=3):
        """Process OCR results to get unique numbers in lines."""
        all_digits = [
            item for result in ocr_results for item in self.split_digits(result)
        ]

        line_groups = []
        for bbox1, digit1 in all_digits:
            added_to_line = False
            for line in line_groups:
                if any(self.is_on_same_line(bbox1, bbox2) for bbox2, _ in line):
                    line.append((bbox1, digit1))
                    added_to_line = True
                    break
            if not added_to_line:
                line_groups.append([(bbox1, digit1)])

        lines = ["".join(digit for _, digit in line) for line in line_groups]

        if lines == previous_texts:
            self.repeat_count += 1
            if self.repeat_count >= repeat_threshold and lines:
                return None
        else:
            self.repeat_count = 0

        return lines

    def extract_scoring_index(self, line):
        """Extract scoring index from a line of numbers."""
        zero_index = line.find("0")
        if zero_index != -1:
            score = line[zero_index + 1 :]
            if score:
                return f"20/{line[:zero_index]}"
        return None

    def return_ocr_result(self, img):
        self.repeat_count = 0

        # Read the image
        img_path = img
        frame = cv2.imread(img_path)

        if frame is None:
            print("Error: Image not found or cannot be loaded.")
            return None, None

        # Instance text detection
        reader = easyocr.Reader(["en"], gpu=False)

        threshold = 0.1
        previous_texts = []
        actual_output = []

        # try:
        text_raw = reader.readtext(frame)
        current_results = [
            (bbox, text, score) for bbox, text, score in text_raw if score > threshold
        ]

        output = self.process_ocr_results(current_results, previous_texts)
        actual_output.append(output)
        if output is None:
            print("Repeated results. Breaking loop.")
            return None, None

        # Draw bounding boxes and texts
        for bbox, text, score in current_results:
            if score > threshold:
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                if (
                    len(top_left) == 2 and len(bottom_right) == 2
                ):  # Ensure valid coordinates
                    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 5)
                    cv2.putText(
                        frame,
                        text,
                        top_left,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        2,
                    )

        previous_texts = output
        print("Processed OCR Output:", output)

        # Display the image with drawn rectangles and text
        cv2.imshow("Text Recognition", frame)
        # cv2.waitKey(0)  # Wait indefinitely until a key is pressed
        cv2.destroyAllWindows()

        # except Exception as e:
        #     print("ERROR OCCUR", e)
        #     return None, None

        final_output = []
        scoring_index = []

        # Process final output to extract scoring index
        print("Output: ", output)

        # Output:  ['6096824', '0084846', '443242', '3042633']
        # Result should be

        # Scoring Index: ['20/60', '20/84', '20/44', '20/30']
        # Final Output: ['96824', '84846', '43242', '42633']
        final_output = []
        scoring_index = []

        # Process the output
        for line in output:
            temp_output = []
            temp_score = []

            line_length = len(line)

            for j in range(1, line_length):
                temp_score = line[:j]
                if line.endswith(temp_score):
                    temp_output = line[j : line_length - j]
                    break

            final_output.append("".join(temp_output))
            scoring_index.append("".join(temp_score))
        # Convert to dictionary
        result_dict = {out: score for out, score in zip(final_output, scoring_index)}

        print("Final Output:", final_output)
        print("Scoring Index:", scoring_index)
        print("Result Dictionary:", result_dict)

        return final_output, scoring_index
