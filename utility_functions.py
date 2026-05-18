import random

def rndm_color():
    """ Returns a random color in hex """
    digits = '0123456789abcdef'
    hex_color = '#'

    for i in range(6):
        hex_color += digits[random.randint(0, len(digits)-1)]

    return hex_color


def score_to_txt(hi_score=0, mode="r"):
    """ In "r" read mode it returns the already saved score.
        In "w" write mode you can save new High scores in it. """
    
    with open("save_hi_scores/hi_score.txt", "r+") as file:
        if mode == "w":
            file.write(f"HI-SCORE: {str(hi_score)}")
        else:
            file.seek(10)
            return file.read()
    


