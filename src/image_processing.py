import easyocr  # type: ignore
import cv2  # type: ignore


class Image_processing:

    def __init__(self):
        self.repeat_count = 0

    def preprocess_image(self, img_path):
        """Preprocess the image for better OCR performance."""
        frame = cv2.imread(img_path)
        if frame is None:
            raise ValueError("Image not found or cannot be loaded.")
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        
        return thresh

    def enhance_image(self, img):
        """Enhance the image to highlight text."""
        edges = cv2.Canny(img, 100, 200)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(edges, kernel, iterations=1)
        return dilated

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
            score = line[zero_index + 1:]
            if score:
                return f"20/{line[:zero_index]}"
        return None

    def return_ocr_result(self):
        self.repeat_count = 0

        # Read and preprocess the image
        img_path = "/Users/ammaster10/Documents/Github/Visual-Acuity/IMG_1269.jpg"
        preprocessed_image = self.preprocess_image(img_path)
        cv2.imshow("Preprocessed Image", preprocessed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        enhanced_image = self.enhance_image(preprocessed_image)
        cv2.imshow("Enhanced Image", enhanced_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Instance text detection
        reader = easyocr.Reader(["en"], gpu=False)

        # Read text from image
        text_raw = reader.readtext(enhanced_image, min_size=10, detail=1, paragraph=False)
        print("Raw OCR Results:", text_raw)

        current_results = [
            (bbox, text, score) for bbox, text, score in text_raw if score > 0.5
        ]

        previous_texts = []
        output = self.process_ocr_results(current_results, previous_texts)
        if output is None:
            print("Repeated results. Breaking loop.")
            return None, None

        # Draw bounding boxes and texts
        frame = cv2.imread(img_path)
        for bbox, text, score in current_results:
            if score > 0.5:
                print(f"Drawing text: {text} with score: {score}")
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                if len(top_left) == 2 and len(bottom_right) == 2:
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
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        final_output = []
        scoring_index = []

        # Process final output to extract scoring index
        print("Output: ", output)
        # Case of 40 46783 40

        # Return result of final_output 46783 and scoring 40

        for line in output:
            temp_output = []
            temp_score = []
            j = 0
            for i in line:

                if j == 0 and i.isdigit() and int(i) > 0:
                    temp_score.append(i)
                elif j < 3 and i == "0":
                    temp_score.append(i)
                elif i.isdigit() and int(i) > 0:
                    temp_output.append(i)
                elif j >= 3 and i == "0":
                    temp_output.pop()
                    break
                j += 1

            final_output.append(("".join(temp_output)))
            scoring_index.append(("".join(temp_score)))

        # Convert to dictionary
        result_dict = {int(out): int(score) for out, score in zip(final_output, scoring_index) if out.isdigit() and score.isdigit()}

        print("Final Output:", final_output)
        print("Scoring Index:", scoring_index)
        print("Result Dictionary:", result_dict)

        return final_output, scoring_index
