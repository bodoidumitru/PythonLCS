
import pandas as pd


def find_lcs(text1, text2):
    # Создаем таблицу для вычисления длины LCS
    n = len(text1)
    m = len(text2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Заполняем таблицу
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    # Восстанавливаем саму подпоследовательность
    result = []
    i = n
    j = m

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            result.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()

    return "".join(result)


def analyze_csv(input_file, output_file):
    # Читаем CSV
    data = pd.read_csv(input_file)

    # В файле должны быть колонки Text1 и Text2
    results = []

    for _, row in data.iterrows():
        text1 = str(row["Text1"])
        text2 = str(row["Text2"])

        lcs = find_lcs(text1, text2)

        results.append({
            "Text1": text1,
            "Text2": text2,
            "LCS": lcs,
            "LCS_Length": len(lcs)
        })

    # Сохраняем результат
    result_data = pd.DataFrame(results)
    result_data.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(result_data)
    print("\nРезультат сохранен в", output_file)


# Запуск программы
analyze_csv("input.csv", "result.csv")
