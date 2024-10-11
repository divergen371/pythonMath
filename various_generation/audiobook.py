# Standard Library
from tkinter import Tk, filedialog

# Third Party Library
import PyPDF2
import pyttsx3


def browse_file() -> str:
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF", filetypes=[("PDF Files", "*.pdf")]
    )
    return file_path


def pdf_to_audio(file_path: str) -> None:
    pdf_reader = PyPDF2.PdfReader(open(file_path, "rb"))
    speaker = pyttsx3.init()

    for page_num in range(len(pdf_reader.pages)):
        text = pdf_reader.pages[page_num].extract_text()
        speaker.say(text=text)
        speaker.runAndWait()

    speaker.stop()
    return None


if __name__ == "__main__":
    pdf_file = browse_file()
    if pdf_file:
        pdf_to_audio(pdf_file)
    else:
        print("No file selected.")
