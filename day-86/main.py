import tkinter as tk
from Faker import Faker
import time

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        self.fake_instance = Faker()
        self.fake_sentence = self.fake_instance.get_sentence()['content']

        self.start_time = None

        self.create_widgets()

    def create_widgets(self):
        self.sentence_text = tk.Text(self.root, height=4, width=50, wrap='word', state='disabled', bg='white', font=('Arial', 12))
        self.sentence_text.pack(pady=20)
        self.update_sentence_display()

        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack(pady=20)
        self.text_entry.bind('<KeyRelease>', self.check_input)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=20)

        self.generate_button = tk.Button(self.root, text="Generate Random Sentence", command=self.generate_new_sentence)
        self.generate_button.pack(pady=20)

    def update_sentence_display(self):
        self.sentence_text.config(state='normal')
        self.sentence_text.delete('1.0', tk.END)

        self.sentence_text.insert(tk.END, self.fake_sentence)
        self.sentence_text.config(state='disabled')

    def generate_new_sentence(self):

        self.fake_sentence = self.fake_instance.get_new_sentence()['content']
        self.update_sentence_display()
        self.text_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_time = None

    def check_input(self, event):
        user_input = self.text_entry.get()

        if not self.start_time:
            self.start_time = time.time()

        self.sentence_text.config(state='normal')
        self.sentence_text.tag_delete('correct')
        self.sentence_text.tag_delete('incorrect')

        for index, (sentence_char, input_char) in enumerate(zip(self.fake_sentence, user_input)):
            if sentence_char == input_char:
                self.sentence_text.tag_add('correct', '1.0+%dc' % index, '1.0+%dc' % (index + 1))
                self.sentence_text.tag_config('correct', foreground='green')
            else:
                self.sentence_text.tag_add('incorrect', '1.0+%dc' % index, '1.0+%dc' % (index + 1))
                self.sentence_text.tag_config('incorrect', foreground='red')

        if user_input == self.fake_sentence:
            elapsed_time = time.time() - self.start_time
            typing_speed = len(self.fake_sentence.split()) / (elapsed_time / 60) 
            
            self.result_label.config(text=f"Well done! Typing speed: {typing_speed:.2f} words per minute.")
        elif self.fake_sentence.startswith(user_input):
            pass
        else:
            self.result_label.config(text="Typing error, please try again.")

def main():
    root = tk.Tk()
    TypingTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
