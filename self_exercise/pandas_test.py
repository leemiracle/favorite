"""
为什么要用pandas？ 针对需要做数据分析的人用的
优点
    1.快：适合处理报表类的数据【数据分析】【数据并行】
    2.代码量少【容易维护】
缺点：不适合每个变量间的逻辑特别复杂的情形
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Chipotle_exercise():
    """ todo 统计指标"""
    # uri = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv'
    uri = 'chipotle.tsv'
    chipo = pd.read_csv(uri, sep='\t') #直接可以从网上下载

    """ 基本信息 
    	order_id	quantity	item_name	choice_description	item_price
    0	1	1	Chips and Fresh Tomato Salsa	NaN	$2.39</td> </tr> <tr> <th>1</th> <td>1</td> <td>1</td> <td>Izze</td> <td>[Clementine]</td> <td>$3.39
    2	1	1	Nantucket Nectar	[Apple]	$3.39</td> </tr> <tr> <th>3</th> <td>1</td> <td>1</td> <td>Chips and Tomatillo-Green Chili Salsa</td> <td>NaN</td> <td>$2.39
    """

    # 前十
    print("前十:", chipo.head(10))
    # 多少个数据：
    # Solution 1
    print("多少条记录:", chipo.shape[0])
    # Solution 2
    print("数据结构信息:", chipo.info())
    print("多少列:", chipo.shape[1])
    print("所有的列名: ", chipo.columns)
    print("数据集是如何创建索引?: ", chipo.index)

    c = chipo.groupby('item_name')
    c = c.sum()
    c = c.sort_values(['quantity'], ascending=False)
    print("被点的最多的商品?", c.head(1))
    print("点的最多的商品，被点了多少份?", c.head(1))
    print("点的最多的商品的描述?", c.head(1))
    total_items_orders = chipo.quantity.sum()
    print("总共点了多少分商品?", total_items_orders)
    before_type = chipo.item_price.dtype
    dollarizer = lambda x: float(x[1:-1])
    chipo.item_price = chipo.item_price.apply(dollarizer)
    after_type = chipo.item_price.dtype
    print(" 将商品价格转换成float：{}, {}".format(before_type, after_type))
    revenue = (chipo['quantity'] * chipo['item_price']).sum()
    print("这一时期的收入多少：", str(np.round(revenue, 2)))
    print("总共有多少份订单：", chipo.order_id.value_counts().count())
    chipo['revenue'] = chipo['quantity'] * chipo['item_price']
    order_grouped = chipo.groupby(by=['order_id']).sum()
    print("每份订单中平均消费多少：", order_grouped.mean()['item_price'])
    print("有多少种不同的商品：", chipo.item_name.value_counts().count()) # value_counts:unique值计数

    """ 过滤和排序"""
    # 数据清洗
    prices = [float(value[1: -1]) for value in chipo.item_price]
    chipo.item_price = prices # 转换成float变量：
    # make the comparison
    chipo10 = chipo[chipo['item_price'] > 10.00]
    chipo10.head()
    len(chipo10)
    # #################单价从高到低排
    # delete the duplicates in item_name and quantity
    chipo_filtered = chipo.drop_duplicates(['item_name', 'quantity'])

    # select only the products with quantity equals to 1
    chipo_one_prod = chipo_filtered[chipo_filtered.quantity == 1]

    # select only the item_name and item_price columns
    price_per_item = chipo_one_prod[['item_name', 'item_price']]

    # sort the values from the most to less expensive
    price_per_item.sort_values(by="item_price", ascending=False)
    chipo.item_name.sort_values()
    ###### 最贵的
    chipo.sort_values(by="item_price", ascending=False).head(1)
    ###### 具体的菜的统计
    chipo_salad = chipo[chipo.item_name == "Veggie Salad Bowl"]
    len(chipo_salad)
    #### 两种过滤条件
    chipo_drink_steak_bowl = chipo[(chipo.item_name == "Canned Soda") & (chipo.quantity > 1)]
    len(chipo_drink_steak_bowl)


def Occupation_exercise():
    """todo 对类行列式或者表格信息处理 """
    # uri = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/u.user"
    data_file = "Occupation.user"
    users = pd.read_table(data_file,
                          sep='|', index_col='user_id')
    users.head(25)
    users.tail(10)
    users.shape[0]
    users.shape[1]
    users.columns
    users.index
    users.dtypes
    # 查看列值
    users.occupation
    users['occupation']
    # unique种类
    users.occupation.nunique()
    # occupation频率最高的
    users.occupation.value_counts().head() # value_counts就会排序
    users.describe() # 总体汇总
    users.describe(include="all") # 汇总所有列
    users.occupation.describe() # 单独occupation
    round(users.age.mean())
    users.age.value_counts().tail(1) # 年龄最小的

    ####### 选择职业的男性占比【male->1】 todo group by
    def gender_to_numeric(x):
        if x == 'M':
            return 1
        if x == 'F':
            return 0
    # apply the function to the gender column and create a new column：【applymap：应用于每个元素，apply应用在一维向量上， map是作用在Series 上】
    users['gender_n'] = users['gender'].apply(gender_to_numeric)
    a = users.groupby('occupation').gender_n.sum() / users.occupation.value_counts() * 100
    # sort to the most male
    a.sort_values(ascending=False)
    #
    users.groupby(['occupation', 'gender']).age.mean()

    # create a data frame and apply count to gender
    gender_ocup = users.groupby(['occupation', 'gender']).agg({'gender': 'count'})

    # create a DataFrame and apply count for each occupation：将一个函数使用在一个数列上，然后返回一个标量的值。
    occup_count = users.groupby(['occupation']).agg('count')

    # divide the gender_ocup per the occup_count and multiply per 100
    occup_gender = gender_ocup.div(occup_count, level="occupation") * 100

    # present all rows from the 'gender column'
    occup_gender.loc[:, 'gender']


def World_Food_Facts():
    """todo: kaggle problem 找到自己要的数据
    """
    food = pd.read_csv('~/Desktop/en.openfoodfacts.org.products.tsv', sep='\t')
    food.shape
    food.columns[104] # 105th: -glucose_100g
    food.dtypes['-glucose_100g']
    food.index
    food.values[18][7]


def group_Alcohol_Consumption():
    drinks = pd.read_csv('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv')
    drinks.head()
    # 不同continent，喝啤酒的平均值
    drinks.groupby('continent').beer_servings.mean()
    # 红酒消费的统计信息：【count mean std min 25% 50% 75% max】
    drinks.groupby('continent').wine_servings.describe()
    # 中位数
    drinks.groupby('continent').median()
    # 统计信息
    drinks.groupby('continent').spirit_servings.agg(['mean', 'min', 'max'])


def auto_mpg():
    """todo 每加仑英里： UC Irvine Machine Learning Repository 数据拼接"""
    cars1 = pd.read_csv(
        "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/05_Merge/Auto_MPG/cars1.csv")
    cars2 = pd.read_csv(
        "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/05_Merge/Auto_MPG/cars2.csv")
    print(cars1.head())
    print(cars2.head())
    # 清洗多余的列
    cars1 = cars1.loc[:, "mpg":"car"]
    cars1.head()
    # 单纯数据合并
    cars = cars1.append(cars2)

    raw_data_1 = {
        'subject_id': ['1', '2', '3', '4', '5'],
        'first_name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
        'last_name': ['Anderson', 'Ackerman', 'Ali', 'Aoni', 'Atiches']}

    raw_data_2 = {
        'subject_id': ['4', '5', '6', '7', '8'],
        'first_name': ['Billy', 'Brian', 'Bran', 'Bryce', 'Betty'],
        'last_name': ['Bonder', 'Black', 'Balwner', 'Brice', 'Btisan']}

    raw_data_3 = {
        'subject_id': ['1', '2', '3', '4', '5', '7', '8', '9', '10', '11'],
        'test_id': [51, 15, 15, 61, 16, 14, 15, 1, 61, 16]}
    data1 = pd.DataFrame(raw_data_1, columns=['subject_id', 'first_name', 'last_name'])
    data2 = pd.DataFrame(raw_data_2, columns=['subject_id', 'first_name', 'last_name'])
    data3 = pd.DataFrame(raw_data_3, columns=['subject_id', 'test_id'])
    # 列完全不变，将row数据按顺序组合【索引不变】
    all_data = pd.concat([data1, data2])
    # 行索引不变：按顺序 组合 列数据
    all_data_col = pd.concat([data1, data2], axis=1)
    # 相同的subject_id，则将data3的列拼接在all_data后
    pd.merge(all_data, data3, on='subject_id')
    # 只拼接 data1和data2的subject_id值相同的列
    pd.merge(data1, data2, on='subject_id', how='inner')
    # 拼接成笛卡尔集
    pd.merge(data1, data2, on='subject_id', how='outer')


def Titanic_Desaster():
    """todo Visualizing kaggle 可视化"""
    url = 'https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/Visualization/Titanic_Desaster/train.csv'
    titanic = pd.read_csv(url)
    url = 'https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/09_Time_Series/Apple_Stock/appl_1980_2014.csv'
    apple = pd.read_csv(url)


def Apple_Stock():
    """todo 股票市场交易等 是时间强相关的"""
    url = 'https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/09_Time_Series/Apple_Stock/appl_1980_2014.csv'
    apple = pd.read_csv(url)
    apple.head()
    apple.Date = pd.to_datetime(apple.Date)
    # 设置成索引
    apple = apple.set_index('Date')
    # 每个月的最后一个工作日
    apple_month = apple.resample('BM').mean()

    # 删除数据：单个数据设置成NA， del 列， dropna(how='any')【丢弃包含na的行】


if __name__ == '__main__':
    Chipotle_exercise()
