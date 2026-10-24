import pandas as pd

def find_lcs(text1, text2):
    n, m = len(text1), len(text2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = []
    i, j = n, m
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
    data = pd.read_csv(input_file, keep_default_na=False)
    required = {"Text1", "Text2"}
    if not required.issubset(data.columns):
        raise ValueError("CSV must contain columns named Text1 and Text2")

    results = []
    for _, row in data.iterrows():
        text1, text2 = str(row["Text1"]), str(row["Text2"])
        lcs = find_lcs(text1, text2)
        results.append({
            "Text1": text1,
            "Text2": text2,
            "LCS": lcs,
            "LCS_Length": len(lcs),
            "Text1_Length": len(text1),
            "Text2_Length": len(text2)
        })

    result_data = pd.DataFrame(results)
    result_data.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(result_data[["LCS", "LCS_Length", "Text1_Length", "Text2_Length"]])
    print(f"\nSaved results to: {output_file}")

if __name__ == "__main__":
    input_file = input("Enter input CSV filename (e.g. 01_text_comparison.csv): ").strip()
    output_file = input("Enter output CSV filename (e.g. result.csv): ").strip()
    analyze_csv(input_file, output_file)
