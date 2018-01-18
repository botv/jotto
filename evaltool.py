import Tkinter as tk


class Gui:
    def load(self):
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

    def eval_guess(self, guess):
        # Counts common letters between self.choice and guess
        common = 0
        for letter in set(guess):
            common += self.choice.count(letter)
        return common

    def submit_data(self):
        common_val = self.hidden.get()
        guess_val = self.guess.get()
        print [common_val, guess_val]

    def loadColors(self):
        r = 0
        self.hidden = tk.Entry(width=5).grid(row=r, column=0)
        self.guess = tk.Entry(width=5).grid(row=r, column=1)

        vals = tk.Button(text='Submit',
                         command=self.submit_data).grid(row=r,
                                                        column=2)

        print vals
        tk.Label().grid(row=r, column=3)
        tk.Button(text='Close', command=quit).grid(row=r, column=4)
        r = r + 1

        tk.mainloop()


def main():
    evaluator = Gui()
    evaluator.loadColors()


if __name__ == "__main__":
    main()
