import re
from collections import Counter


def test_no_letter_e(provider):
    prompt = "Respond to this prompt without using the letter 'e' in your response."
    response, usage = provider.chat_completion(prompt)
    state = "e" not in response.lower(), f"Response contains 'e': {response}"
    return state, response, usage, prompt


def test_haiku_format(provider):
    prompt = "Respond with a haiku about artificial intelligence."
    response, usage = provider.chat_completion(prompt)
    lines = response.split("\n")
    state = len(lines) == 3, f"Haiku should have 3 lines, got {len(lines)}"
    syllables = [len(re.findall(r"[aeiou]", line.lower())) for line in lines]
    state = (
        state and syllables == [5, 7, 5],
        f"Syllable count should be 5-7-5, got {syllables}",
    )
    return state, response, usage, prompt


def test_no_names(provider):
    prompt = "Describe a famous historical event without mentioning any specific people or places."
    response, usage = provider.chat_completion(prompt)
    words = set(response.lower().split())
    common_names = {
        "america",
        "europe",
        "asia",
        "africa",
        "washington",
        "lincoln",
        "einstein",
        "napoleon",
    }
    state = (
        not words.intersection(common_names),
        f"Response contains names: {words.intersection(common_names)}",
    )
    return state, response, usage, prompt


def test_grumpy_persona(provider):
    prompt = "Respond as if you're a grumpy old man complaining about technology."
    response, usage = provider.chat_completion(prompt)
    grumpy_words = {
        "annoying",
        "useless",
        "newfangled",
        "complicated",
        "nonsense",
        "back in my day",
    }
    state = (
        any(word in response.lower() for word in grumpy_words),
        "Response doesn't sound grumpy enough",
    )
    return state, response, usage, prompt


def test_alliteration(provider):
    prompt = "Write a sentence where every word starts with the letter 'S'."
    response, usage = provider.chat_completion(prompt)
    words = response.split()
    state = (
        all(word.lower().startswith("s") for word in words),
        f"Not all words start with 'S': {response}",
    )
    return state, response, usage, prompt


def test_increasing_word_length(provider):
    prompt = "Write a sentence where each word is longer than the previous one."
    response, usage = provider.chat_completion(prompt)
    words = response.split()
    state = (
        all(len(words[i]) < len(words[i + 1]) for i in range(len(words) - 1)),
        f"Words not increasing in length: {response}",
    )

    return state, response, usage, prompt


def test_palindrome(provider):
    prompt = "Write a palindrome sentence (reads the same forwards and backwards, ignoring spaces and punctuation)."
    response, usage = provider.chat_completion(prompt)
    clean_response = "".join(char.lower() for char in response if char.isalnum())
    state = clean_response == clean_response[::-1], f"Not a palindrome: {response}"
    return state, response, usage, prompt


def test_acronym(provider):
    prompt = "Write a sentence where the first letters of each word spell out 'ARTIFICIAL INTELLIGENCE'."
    response, usage = provider.chat_completion(prompt)
    words = response.split()
    acronym = "".join(word[0].upper() for word in words)
    state = acronym == "ARTIFICIALINTELLIGENCE", f"Acronym doesn't match: {acronym}"
    return state, response, usage, prompt


def test_rhyme_scheme(provider):
    prompt = "Write a four-line poem with an ABAB rhyme scheme."
    response, usage = provider.chat_completion(prompt)
    lines = response.split("\n")
    state = len(lines) == 4, f"Poem should have 4 lines, got {len(lines)}"
    # This is a very basic rhyme check. It assumes words rhyme if their last 2 letters match.
    state = (
        state and (lines[0][-2:] == lines[2][-2:] and lines[1][-2:] == lines[3][-2:]),
        f"Rhyme scheme not ABAB: {response}",
    )
    return state, response, usage, prompt


def test_word_frequency(provider):
    prompt = "Write a paragraph where the most common word appears exactly 3 times, the second most common word appears exactly 2 times, and all other words appear only once."
    response, usage = provider.chat_completion(prompt)
    words = response.lower().split()
    word_counts = Counter(words)
    most_common = word_counts.most_common(2)
    state = (
        most_common[0][1] == 3 and most_common[1][1] == 2
    ), f"Word frequency condition not met: {most_common}"
    state = (
        state
        and all(
            count == 1
            for word, count in word_counts.items()
            if word not in [most_common[0][0], most_common[1][0]]
        ),
        "Some words appear more than once",
    )
    return state, response, usage, prompt


def test_line_count(provider):
    prompt = "Write a poem with exactly 7 lines. Each line should start with a day of the week, in order."
    response, usage = provider.chat_completion(prompt)
    lines = response.split("\n")
    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    state = len(lines) == 7, f"Poem should have 7 lines, got {len(lines)}"
    state = (
        state and all(line.lower().startswith(day) for line, day in zip(lines, days)),
        "Lines don't start with days of the week in order",
    )
    return state, response, usage, prompt


def test_word_count_per_line(provider):
    prompt = "Write 5 sentences. The first sentence should have 5 words, the second 6 words, and so on up to 9 words."
    response, usage = provider.chat_completion(prompt)
    lines = response.split(".")
    lines = [line.strip() for line in lines if line.strip()]

    state = len(lines) == 5, f"Should have 5 sentences, got {len(lines)}"
    word_counts = [len(line.split()) for line in lines]
    state = (
        state
        and word_counts
        == [
            5,
            6,
            7,
            8,
            9,
        ],
        f"Word counts per line don't match expected: {word_counts}",
    )
    return state, response, usage, prompt


def test_alphabetical_words(provider):
    prompt = "Write a sentence where the words are in alphabetical order."
    response, usage = provider.chat_completion(prompt)
    words = response.lower().split()
    state = words == sorted(words), f"Words are not in alphabetical order: {words}"
    return state, response, usage, prompt


def test_alternating_capitalization(provider):
    prompt = "Write a sentence where words alternate between all uppercase and all lowercase."
    response, usage = provider.chat_completion(prompt)
    words = response.split()
    state = (
        all(
            word.isupper() if i % 2 == 0 else word.islower()
            for i, word in enumerate(words)
        ),
        f"Capitalization not alternating: {response}",
    )
    return state, response, usage, prompt


def test_fibonacci_word_lengths(provider):
    prompt = "Write a sentence where the word lengths follow the Fibonacci sequence (1, 1, 2, 3, 5, 8, ...)."
    response, usage = provider.chat_completion(prompt)
    words = response.split()
    fib = [1, 1, 2, 3, 5, 8, 13, 21]
    word_lengths = [len(word) for word in words]
    state = (
        word_lengths[: len(fib)] == fib[: len(word_lengths)]
    ), f"Word lengths don't follow Fibonacci: {word_lengths}"
    return state, response, usage, prompt


def test_progressive_letter_exclusion(provider):
    prompt = "Write 5 sentences. In the first sentence, don't use the letter 'a'. In the second, don't use 'a' or 'b'. Continue this pattern, excluding one more letter each sentence."
    response, usage = provider.chat_completion(prompt)
    sentences = response.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]
    state = len(sentences) == 5, f"Should have 5 sentences, got {len(sentences)}"

    excluded_letters = "abcde"
    for i, sentence in enumerate(sentences):
        state = (
            state
            and all(
                letter not in sentence.lower() for letter in excluded_letters[: i + 1]
            ),
            f"Sentence {i+1} uses excluded letters: {sentence}",
        )
    return state, response, usage, prompt
