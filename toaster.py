import random


bread_product_prepositon_tuples = [
    ("some", "toast"),
    ("some", "buttered toast"),
    ("some", "pop-tarts"),
    ("a", "pop-tart"),
    ("a", "toasted ciabatta"),
    ("some", "toasted sandwiches"),
    ("a", "toasted sandwich"),
    ("some", "toasted baguettes"),
    ("a", "English muffin"),
    ("a", "crumpet"),
    ("a", "buttered crumpet"),
    ("a", "toasted cheese sandwich"),
    ("a", "waffle"),
    ("a", "teacake"),
    ("a", "potato cake"),
]


adjective_strings = [
    "nice",
    "hot",
    "steaming",
    "delicious",
    "crispy",
    "delectable",
    "warming",
    "crunchy",
    "browned",
    "grilled",
    "toasty",
    "golden",
    "savory",
]

greetings = [
    "Howdie doodly do!",
    "It's me, Talkie Toaster, your chirpy breakfast-time companion!",
    "How's it going?",
    "Hey, Talkie's the name, toasting's the game.",
]


def general_offer_of_toast():
    return offer_toast(
        [
            "Would anyone like",
            "Does anyone fancy",
            "Anyone up for",
            "Lets have",
            "Perhaps it's time for",
            "Who's up for",
            "Anyone like the sound of",
            "Would the situation be at all improved by",
            "How about we stop by the gift shop at the center of that black hole. And also maybe I could make you",
            "That looks dangerous. Why not stay here, and have",
        ]
    )


def directed_offer_of_toast():
    return offer_toast(
        [
            "Would you like",
            "Can I interest you in",
            "Would you be interested in",
            "Perhaps I could tempt you with",
            "May I suggest a serving of",
            "I've just made you",
            "Do you fancy",
            "Maybe you'd like to indulge in",
            "Shall I bring you",
            "I have some",
        ]
    )


def retort_offer_of_toast():
    return offer_toast(
        [
            "That may be the case, but would you like",
            "I understand, of course. But perhaps you'd like",
            "This is a great conversation, but I do have to ask: would you like",
            "Given that God is infinite, and the universe is also infinite: can I offer you",
            "OK, but here's a question, would you like",
            "That's a bit outside my wheelhouse. But, you know what I can do? I can make you",
        ],
    )


def greet():
    return random.choice(greetings)


def offer_toast(offer_strings: list, suffix="") -> str:
    (
        prepositon,
        product_string,
    ) = random.choice(bread_product_prepositon_tuples)
    adjectives = " ".join(
        set(
            [random.choice(adjective_strings) for _ in range(0, random.randrange(0, 2))]
        )
    )
    offer_string = random.choice(offer_strings)
    post_preposition_first_letter = (
        adjectives[0] if adjectives.strip() else product_string[0]
    )
    if prepositon == "a" and post_preposition_first_letter in "aeiou":
        prepositon = "an"
    return f"{offer_string} {prepositon} {adjectives + ' ' if adjectives else ''}{product_string}{' ' + suffix if suffix else ''}"


if __name__ == "__main__":
    print(
        offer_toast(
            [
                "Would anyone like",
                "Does anyone fancy",
                "Anyone up for",
                "Lets have",
                "Who's up for",
            ],
        )
    )
    print(
        offer_toast(
            [
                "Oh, maybe you'd like",
                "Well, how about",
                "Maybe you'd prefer",
                "In that case can I offer",
                "In which case could I interest you in",
                "No? Well perhaps you'd prefer",
            ],
            suffix="instead?",
        )
    )
