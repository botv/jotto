import Tkinter as tk


class Evaluator:
    def load_test1(self):
        root = tk.Tk()
        root.title("Evaluation Tool")
        root.minsize(400, 400)
        root.maxsize(400, 400)
        root.resizable(width=False, height=False)
        hidden = tk.Entry(root, text="Hidden").grid(row=0, column=0)
        hidden.pack(side='bottom')
        guess = tk.Entry(root, text="Hidden").grid(row=0, column=1)
        guess.pack(side='bottom')
        submit = tk.Button(root, text="Close",
                           command=root.quit).grid(row=0, column=2)
        submit.pack(side='bottom')
        close = tk.Button(root, text="Close",
                          command=root.quit).grid(row=0, column=3)
        close.pack(side='bottom')
        root.mainloop()

    def load_test2(self):
        r = 0
        hidden = tk.Entry(width=5)
        hidden.pack()
        hidden.focus_set()
        guess = tk.Entry(width=5)
        guess.pack()
        guess.focus_set()

        def submit_data():
            common_val = hidden.get()
            guess_val = guess.get()
            print [common_val, guess_val]
        tk.Button(text='Submit', command=submit_data).grid(row=r,
                                                           column=2)
        tk.Button(text='Close', command=quit).grid(row=r, column=4)
        tk.mainloop()

    def load_test3(self):
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
    evaluator.load_test3()


if __name__ == "__main__":
    main()
