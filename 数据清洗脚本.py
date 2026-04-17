# --------------------------
# 【1】导入需要用的工具包
# --------------------------
import sys                  # sys：系统相关工具，用来解决中文乱码
import pandas as pd         # pandas：处理表格数据（读csv、删空值、替换等）
import numpy as np          # numpy：数学计算（这里主要配合pandas使用）


# --------------------------
# 【2】解决 Windows 终端中文乱码
# --------------------------
sys.stdout.reconfigure(encoding='utf-8')
# sys.stdout           = 控制台输出
# reconfigure          = 重新设置
# encoding='utf-8'     = 把输出编码改成 utf-8，中文就不乱码


# --------------------------
# 【3】读取 CSV 数据文件
# --------------------------
df = pd.read_csv(
    'developer_burnout_dataset_7000.csv',  # 要读取的文件名
    encoding='utf-8'                       # 文件编码，utf-8 最通用
)
# df = 你整个表格数据，后面所有操作都对 df 进行


# --------------------------
# 【4】查看前 5 行数据
# --------------------------
print("===== 数据前5行 =====")
print(df.head())
# head()       = 默认显示前5行
# head(10)     = 显示前10行（括号里数字就是行数）


# --------------------------
# 【5】查看数据基本信息（列名、类型、有无空值）
# --------------------------
print("\n===== 数据基本信息 =====")
df.info()
# info() 会输出：
# - 多少行、多少列
# - 每列有多少非空值
# - 每列是什么类型（数字/文字）


# --------------------------
# 【6】统计重复行总数
# --------------------------
print("\n===== 重复行数量 =====")
dup_count = df.duplicated(keep=False).sum()
print("重复行总数：", dup_count)

# duplicated()        = 判断每一行是不是重复行
# keep=False          = 所有重复行都标记为 True（包括第一次出现的）
# sum()               = 把 True 当1、False当0，加起来就是总数


# --------------------------
# 【7】检查整张表有没有空值
# --------------------------
print("="*50)
has_null = df.isnull().any().any()
print("整个表是否存在空值：", has_null)
print("="*50)

# df.isnull()         = 逐个格子判断：空值=True，非空=False
# .any()              = 每一列是否至少一个空值
# .any()              = 所有列中是否至少一列有空值
# 最终结果：True=有空值，False=没有空值


# --------------------------
# 【8】把数值列的空值替换成该列均值
# --------------------------
print("\n===== 开始替换空值为均值 =====")

# 第一步：只选出“数字类型”的列
numeric_cols = df.select_dtypes(include=['number']).columns

# select_dtypes        = 按数据类型筛选列
# include=['number']   = 只包含数字类型（int、float）
# columns              = 拿到这些列的名字

# 第二步：空值 → 替换为每列自己的均值
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# fillna()             = 把空值填充
# df[numeric_cols].mean() = 对每一列计算平均值
# 每列空值 → 用这一列的平均值填充

print("✅ 空值替换完成！")


# --------------------------
# 【9】查看填充后的前5行
# --------------------------
print("\n===== 空值填充后前5行 =====")
print(df.head())


# --------------------------
# 【10】再次检查空值是否真的没了
# --------------------------
print("\n===== 空值检查结果 =====")
print("替换后是否还有空值：", df.isnull().any().any())
print("\n每列剩余空值数量：")
print(df.isnull().sum())

# isnull().sum()       = 统计每一列有多少个空值
# 输出 0 代表这一列没有空值


# --------------------------
# 【11】保存【填充空值后】的数据
# --------------------------
df.to_csv(
    "处理后_无空值数据.csv",   # 保存后的文件名
    index=False,              # 不保存 pandas 自动生成的行号
    encoding="utf-8-sig"      # 保证 Excel 打开中文不乱码
)
print("\n✅ 无空值数据已保存")


# --------------------------
# 【12】删除 burnout_level 为空的行
# --------------------------
df = df.dropna(subset=["burnout_level"])

# dropna()             = 删除有空值的行
# subset=["列名"]      = 只看这一列，这一列空就删除整行

print("\n✅ 已删除 burnout_level 为空的行")


# --------------------------
# 【13】保存【删除空行后】的数据
# --------------------------
df.to_csv(
    "删除空行后.csv",
    index=False,
    encoding="utf-8-sig"
)


# --------------------------
# 【14】只保留数值列，用于异常值检测
# --------------------------
numeric_df = df.select_dtypes(include=['number'])

# 只把数字列拿出来，文字列不参与异常值计算


# --------------------------
# 【15】遍历每一列，检测异常值（IQR方法）
# --------------------------
print("\n===== 开始检测异常值 =====")

for col in numeric_df.columns:
    # 对每一列单独计算
    
    # 四分位数
    Q1 = numeric_df[col].quantile(0.25)   # 25% 分位数（小的那一头）
    Q3 = numeric_df[col].quantile(0.75)   # 75% 分位数（大的那一头）
    
    # 四分位距
    IQR = Q3 - Q1
    
    # 正常范围上下限
    lower_bound = Q1 - 1.5 * IQR   # 下限
    upper_bound = Q3 + 1.5 * IQR   # 上限

    # 找出超出范围的异常值
    outliers = numeric_df[(numeric_df[col] < lower_bound) | (numeric_df[col] > upper_bound)]
    
    # 打印结果
    print(f"========== 列：{col} ==========")
    print(f"正常范围：[{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"异常值数量：{len(outliers)}")
    
    if len(outliers) > 0:
        print("异常值如下：")
        print(outliers[col])
    print()


# --------------------------
# 【16】复制一份原数据，避免改坏原始表
# --------------------------
df_fixed = df.copy()

# copy() = 完整复制一份数据
# 改 df_fixed，不会影响原来的 df


# --------------------------
# 【17】把异常值替换成该列均值
# --------------------------
for col in numeric_df.columns:
    # 重新算一遍正常范围
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # 标记哪些位置是异常值
    mask = (df_fixed[col] < lower) | (df_fixed[col] > upper)

    # 把异常值替换成这一列的均值
    df_fixed.loc[mask, col] = df_fixed[col].mean()

print("\n✅ 异常值已替换为均值")


# --------------------------
# 【18】保存最终干净数据
# --------------------------
df_fixed.to_csv(
    "处理好的数据.csv",
    encoding='utf-8-sig',
    index=False
)

print("\n========================================")
print("          全部处理完成！")
print(" 最终文件：处理好的数据.csv")
print("========================================")
