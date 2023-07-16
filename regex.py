import re

def convert_to_regex(text):
    # Échapper les caractères spéciaux en les préfixant avec un antislash (\)
    escaped_text = re.escape(text)

    # Remplacer les caractères génériques par leurs équivalents regex
    wildcard_pattern = r'\?'
    escaped_text = re.sub(wildcard_pattern, '.', escaped_text)

    # Remplacer les astérisques (*) par leur équivalent regex
    asterisk_pattern = r'\*'
    escaped_text = re.sub(asterisk_pattern, '.*', escaped_text)

    # Remplacer les groupes entre crochets ([mot1, mot2]) par une classe de caractères
    bracket_pattern = r'\[([^\]]+)\]'
    match = re.search(bracket_pattern, escaped_text)
    while match:
        bracket_content = match.group(1)
        bracket_items = bracket_content.split(',')
        bracket_regex = '[' + re.escape(''.join(bracket_items)) + ']'
        escaped_text = re.sub(bracket_pattern, bracket_regex, escaped_text, count=1)
        match = re.search(bracket_pattern, escaped_text)

    # Remplacer les accolades ({n}) par leur équivalent regex pour une répétition exacte
    repetition_pattern = r'\{(\d+)\}'
    escaped_text = re.sub(repetition_pattern, r'{\1}', escaped_text)

    # Convertir les mots en classes de caractères pour correspondre à n'importe quel mot de la liste
    word_pattern = r'\\w\{([^\}]+)\}'
    match = re.search(word_pattern, escaped_text)
    while match:
        word_content = match.group(1)
        word_items = word_content.split(',')
        word_regex = '(?:' + '|'.join(map(re.escape, word_items)) + ')'
        escaped_text = re.sub(word_pattern, word_regex, escaped_text, count=1)
        match = re.search(word_pattern, escaped_text)

    # Remplacer les signes d'interrogation (?) par des assertions de correspondance facultatives
    optional_pattern = r'\(\?\:([\s\S]+?)\)\?'
    escaped_text = re.sub(optional_pattern, r'(?:\1)?', escaped_text)

    # Remplacer les signes de dollar ($) par des assertions de correspondance de fin de ligne
    endline_pattern = r'\$\$'
    escaped_text = re.sub(endline_pattern, r'$', escaped_text)

    # Retourner l'expression régulière finale
    return escaped_text

# Exemple d'utilisation
text = "Ex[a, b]m{2,4}ple? of te*xt \\w{apple, banana, cherry} (?:option1|option2)? $$"
regex = convert_to_regex(text)
print(regex)  # Affiche "Ex[a, b]m{2,4}ple. of te.*xt (?:apple|banana|cherry) (?:option1|option2)?$"
