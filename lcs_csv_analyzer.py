import pandas as pd

# Словарь для транслитерации кириллицы в латиницу
CYRILLIC_TO_LATIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
}

def transliterate(text):
    """Конвертирует русский текст в латиницу и приводит к нижнему регистру."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    result = []
    for char in text:
        if char in CYRILLIC_TO_LATIN:
            result.append(CYRILLIC_TO_LATIN[char])
        else:
            result.append(char)
    return "".join(result)

def find_common_words(text1, text2):
    """
    Находит общие слова (пересечение) между двумя текстами 
    с учетом транслитерации и игнорированием порядка слов.
    """
    t1_norm = transliterate(text1)
    t2_norm = transliterate(text2)
    
    words1 = set(t1_norm.split())
    words2 = set(t2_norm.split())
    
    common = words1.intersection(words2)
    return " ".join(sorted(common))

def find_lcs_translit(text1, text2):
    """Классический LCS посимвольно после приведения к единой латинице."""
    t1 = transliterate(text1)
    t2 = transliterate(text2)
    
    n, m = len(t1), len(t2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if t1[i - 1] == t2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = []
    i, j = n, m
    while i > 0 and j > 0:
        if t1[i - 1] == t2[j - 1]:
            result.append(t1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return "".join(result)

def analyze_csv(input_file, output_file):
    data = pd.read_csv(input_file, keep_default_na=False)
    required = {"Text1", "Text2"}
    if not required.issubset(data.columns):
        raise ValueError("CSV must contain columns named Text1 and Text2")

    results = []
    for _, row in data.iterrows():
        text1, text2 = str(row["Text1"]), str(row["Text2"])
        
        # Поиск совпадений с учетом транслита
        lcs_translit = find_lcs_translit(text1, text2)
        common_words = find_common_words(text1, text2)
        
        results.append({
            "Text1": text1,
            "Text2": text2,
            "Translit_LCS": lcs_translit,
            "Common_Words": common_words,
            "Common_Words_Count": len(common_words.split()) if common_words else 0,
            "Text1_Length": len(text1),
            "Text2_Length": len(text2)
        })

    result_data = pd.DataFrame(results)
    result_data.to_csv(output_file, index=False, encoding="utf-8-sig")
    
    print(result_data[["Text1", "Text2", "Common_Words", "Common_Words_Count"]])
    print(f"\nSaved results to: {output_file}")

if __name__ == "__main__":
    input_file = input("Enter input CSV filename (e.g. 01_text_comparison.csv): ").strip()
    output_file = input("Enter output CSV filename (e.g. result.csv): ").strip()
    analyze_csv(input_file, output_file)
