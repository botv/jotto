import Tkinter as tk


class Evaluator:
    def load(self):
        # Optional common letter evaluation tool
        root = tk.Tk()
        root.title("Jotto Evaluation Tool")
        root.resizable(width=False, height=False)
        options = tk.Frame(root)
        options.pack(side='top')
        # output = tk.Frame(root)
        # output.pack(side='bottom')
        hidden_val = tk.StringVar()
        guess_val = tk.StringVar()
        output_label = tk.Label(options, text="Hidden:")
        output_label.pack(side='left')
        hidden = tk.Entry(options, textvariable=guess_val, width=8)
        hidden.pack(side='left')
        hidden.focus_set()
        output_label = tk.Label(options, text="Guess:")
        output_label.pack(side='left')
        guess = tk.Entry(options, textvariable=hidden_val, width=8)
        guess.pack(side='left')
        guess.focus_set()
        common = tk.StringVar()

        def eval_guess():
            common_out = 0
            guess_eval = guess.get()
            choice = hidden.get()
            all_letters = guess_eval.isalpha() and choice.isalpha()
            if len(guess_eval) == 5 and len(choice) == 5 and all_letters:
                for letter in set(guess_eval):
                    common_out += choice.count(letter)
                    if common_out == 1:
                        common.set("There is 1 common letter.")
                    else:
                        common.set("There are " + str(common_out)
                                   + " common letters.")
            else:
                common.set("There's something wrong with your entry.")

        submit_button = tk.Button(options, text="Submit", width=5,
                                  command=eval_guess)
        submit_button.pack(side='left')
        close_button = tk.Button(options, text='Close', command=quit)
        close_button.pack(side='left')
        output_label = tk.Label(root, relief='sunken',
                                textvariable=common)
        output_label.pack(side='bottom', fill='both')
        tk.mainloop()


def main():
    evaluator = Evaluator()
    evaluator.load()
