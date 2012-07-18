import random

class Laser:
    def __init__(self):
        self.buttons = [0,0,0]

    # is laser ready for operation
    # this might not be needed as laser is powered up all the time
    def is_ready(self):
        val = random.random()
        if val > 0.5:
            return True
        else:
            return False

    # scan once and return buttons states
    # state is 1 if button is actuated after last poll
    def scan(self):
        self.buttons = [0,0,0]
        for i in range(0, len(self.buttons)):
            val = random.random()
            if val > 0.95:
                self.buttons[i] = 1
            else:
                self.buttons[i] = 0
        return self.buttons



if __name__ == "__main__":
    lazor = Laser()
    for i in range(1,10):
        print lazor.is_ready()

    for i in range(0,25):
        pressed_buttons = lazor.scan()
        print pressed_buttons
