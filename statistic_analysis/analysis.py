import pandas as pd
import scipy.stats as stats


def clinical_statistical_analysis(df: pd.DataFrame, continuous_cols: list, categorical_cols: list) -> None:
    print("连续变量的统计分析")
    print("------------------------")
    for col in continuous_cols:
        print(f"变量: {col}")
        mean = df[col].mean()
        median = df[col].median()
        std_dev = df[col].std()
        print(f"平均值: {mean}, 中位数: {median}, 标准差: {std_dev}")
        print("\n")

    print("分类变量的统计分析")
    print("------------------------")
    for col in categorical_cols:
        print(f"变量: {col}")
        counts = df[col].value_counts()
        print("计数:")
        print(counts)
        print("\n")

    print("连续变量的假设检验 - t检验")
    print("-------------------------")
    # 假设我们有两组数据，需要使用t检验进行比较
    group1 = df[df['Group'] == 1]['ContinuousVar']
    group2 = df[df['Group'] == 2]['ContinuousVar']
    t_stat, p_value = stats.ttest_ind(group1, group2)
    print(f"t统计量: {t_stat}, p值: {p_value}")

    print("分类变量的假设检验 - 卡方检验")
    print("--------------------------")
    # 假设我们有两个分类变量，需要使用卡方检验进行关联性分析
    contingency_table = pd.crosstab(df['CategoricalVar1'], df['CategoricalVar2'])
    chi2_stat, p_value, _, _ = stats.chi2_contingency(contingency_table)
    print(f"卡方统计量: {chi2_stat}, p值: {p_value}")


# 示例用法
data = {
    'Age': [25, 30, 35, 28, 40, 45, 38, 42],
    'Gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'Diagnosis': [1, 0, 1, 0, 1, 0, 1, 1],
    'Group': [1, 1, 1, 1, 2, 2, 2, 2],
    'ContinuousVar': [4, 5, 4.5, 6, 5.5, 6.5, 5, 6.2]
}

df = pd.DataFrame(data)

continuous_cols = ['Age', 'ContinuousVar']
categorical_cols = ['Gender', 'Diagnosis']

clinical_statistical_analysis(df, continuous_cols, categorical_cols)
