
def search_knowledge(question):
    with open("knowledge.txt", "r") as file:
        documents = file.readlines()

    question = question.lower().strip(" ?.!")

    # Remove common words from the question
    stop_words = {"what", "is", "the", "capital", "of", "in", "a", "an"}

    question_words = [
        word.strip(".,?!")
        for word in question.split()
        if word.strip(".,?!") not in stop_words
    ]

    matches = []

    for line in documents:
        line_lower = line.lower()

        # Count how many meaningful question words match
        score = sum(
            1 for word in question_words
            if word in line_lower
        )

        if score > 0:
            matches.append((score, line.strip()))

    matches.sort(key=lambda item: item[0], reverse=True)

    # Return only the best match, and only if it is clearly relevant
    if matches and matches[0][0] > (matches[1][0] if len(matches) > 1 else 0):
        return [matches[0][1]]

    return []
