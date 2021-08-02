import blessed
import time
import requests
import random


class TypingTest:
    def __init__(self):
        self.t = blessed.Terminal()

    def __get_prompt(self):
        res = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
        words = res.content.splitlines()
        prompt = random.choices(words, k=25)

        rprompt = ' '.join(w.decode() for w in prompt)
        return rprompt

    def __clear(self):
        print(f'{self.t.home}{self.t.clear}', end='')

    def __at_home(self, text, pl=0):
        padding_left = -1 if pl == 0 else pl
        padding_top = -1
        if padding_left >= self.t.width:
            temp = padding_left
            padding_left = temp % self.t.width
            padding_top = temp // self.t.width

        with self.t.location():
            print(f'{self.t.home}{self.t.move_xy(padding_left, padding_top)}{text}', end='', flush=True)

    def __print_prompt(self, prompt):
        self.__clear()
        self.__at_home(f'{self.t.yellow}{prompt}{self.t.normal}')

    def __print_score(self, mask, prompt, errs, elapsed):
        correct = 0
        for l, r in zip(mask, prompt):
            if l == r:
                correct += 1

        correct -= errs
        percentage = "{:.0%}".format(correct / len(mask))
        wpm = int((len(prompt) / 5) / (elapsed / 60))
        message = f"""WPM: {wpm}
Accuracy: {percentage}\n"""
        print(message)


    def __read_input(self, prompt):
        loc = 0
        mask = list(prompt)
        start = time.time()
        errs = 0
        with self.t.cbreak():
            while loc < len(prompt):
                val = self.t.inkey()
                if val.name == 'KEY_BACKSPACE':
                    if loc != 0:
                        loc -= 1
                        self.__at_home(f'{self.t.yellow}{prompt[loc]}{self.t.normal}', pl=loc)
                    continue

                if val.is_sequence:
                    continue

                if val == prompt[loc]:
                    self.__at_home(f'{self.t.green}{val}{self.t.normal}', pl=loc)
                else:
                    self.__at_home(f'{self.t.red}{prompt[loc]}{self.t.normal}', pl=loc)
                    errs += 1

                mask[loc] = val

                loc += 1
        end = time.time()
        self.__clear()
        self.__print_score(mask, prompt, errs, end-start)


    def start(self):
        prompt = self.__get_prompt()
        self.__print_prompt(prompt)
        self.__read_input(prompt)


if __name__ == '__main__':
    t = TypingTest()
    t.start()