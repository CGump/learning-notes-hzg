# 数据库与SQL学习

## 0. 一些概念

* 数据集合称为**数据库**——Database，DB
* 用来管理数据库的计算机系统称为**数据库管理系统**——Database Management System，DBMS

* DBMS的种类：
  * 层次数据库HDB
  * 关系数据库RDB（SQL server、DB2、MySQL）
  * 面向对象数据库OODB
  * XML数据库XMLDB
  * 键值存储系统KVS

* 表的列（垂直方向）称为**字段**，代表数据项目；表的行（水平方向）称为**记录**，相当于一条数据。
* 行和列的交汇方格称为**单元格**，一个单元格只能输入一个数据。

* DDL（Data Definition Language，数据定义语言）用来创建或者删除存储数据用的数据库以及数据库中的表对象
  * CREATE：创建数据库和表等对象
  * DROP：删除数据库和表等对象
  * ALTER：修改数据库和表等对象的结构
* DML（Data Manipulation Language，数据操纵语言）用来查询或变更表中记录：
  * SELECT：查询表中的数据
  * INSERT：向表中插入新数据
  * UPDATE：更新表中的数据
  * DELETE：删除表中的数据
* DCL（Data Control Language，数据控制语言）用来确认或者取消对数据库中的数据变更。以及用户赋权设定：
  * COMMIT：确认对数据库中的数据进行的变更
  * ROLLBACK：取消对数据库中的数据进行的变更
  * GRANT：赋予用户操作权限
  * REVOKE：取消用户的操作权限
* SQL书写规则
  * SQL语句要以分号（;）结尾
  * SQL语句不区分大小写，但为了理解容易规定
    * 关键字大写
    * 表名的首字母大写
    * 其余（列名等）小写
  * 常数的书写方式固定
    * 字符串和日期常数需要使用单引号（'）括起来
    * 数字常数直接书写
  * 单词需要以半角空格或者换行来分隔

## 1. 数据库和SQL
### 1.1 表的内容

举例时使用的商品表如下
表1-2　商品表

| 商品编号 | 商品名称 | 商品种类 | 销售单价 | 进货单价 | 登记日期   |
| -------- | -------- | -------- | -------- | -------- | ---------- |
| 0001     | T恤衫    | 衣服     | 1000     | 500      | 2009-09-20 |
| 0002     | 打孔器   | 办公用品 | 500      | 320      | 2009-09-11 |
| 0003     | 运动T恤  | 衣服     | 4000     | 2800     |            |
| 0004     | 菜刀     | 厨房用具 | 3000     | 2800     | 2009-09-20 |
| 0005     | 高压锅   | 厨房用具 | 6800     | 5000     | 2009-01-15 |
| 0006     | 叉子     | 厨房用具 | 500      |          | 2009-09-20 |
| 0007     | 擦菜板   | 厨房用具 | 880      | 790      | 2008-04-28 |
| 0008     | 圆珠笔   | 办公用品 | 100      |          | 2009-11-11 |

### 1.2 数据库创建

```mysql
CREATE DATABASE <数据库名称>;
```

### 1.3 表的创建

```sql
CREATE TABLE <表名>
（<列名1> <数据类型> <该列所需约束>，
<列名2> <数据类型> <该列所需约束>，
<列名3> <数据类型> <该列所需约束>，
<列名4> <数据类型> <该列所需约束>，
.
.
.
<该表的约束1>， <该表的约束2>，……）；
```

示例，创建Product表：

```sql
CREATE TABLE Product
(product_id CHAR(4) NOT NULL,
product_name VARCHAR(100) NOT NULL,
product_type VARCHAR(32) NOT NULL,
sale_price INTEGER ,
purchase_price INTEGER ,
regist_date DATE ,
PRIMARY KEY (product_id));
```

`NOT NULL`表示该字段数据必须输入，不能为空；

`PRIMARY KEY （product_id）`表示主键约束，该字段的记录不能重复。

### 1.4 表的删除

```sql
DROP TABLE <表名>;
```

删除了的表是无法恢复的。

### 1.5 表的定义更新

* 表中添加列——ADD COLUMN

```sql
ALTER TABLE <表名> ADD COLUMN <列的定义>;
```

例如，在Product表中加入一列product_name_pinyin，存储100位可变长字符串

```mysql
ALTER TABLE Product ADD COLUMN product_name_pinyin VARCHAR(100);
```

* 表中删除列——DROP COLUMN

```sql
ALTER TABLE <表名> DROP COLUMN <列名>；
```

例如，删除刚才创建的product_name_pinyin列

```mysql
ALTER TABLE Product DROP COLUMN product_name_pinyin;
```

* 向Product表中插入数据

```mysql
START TRANSACTION;
INSERT INTO Product VALUES ('0001', 'T恤衫', '衣服', 1000, 500, '2009-09-20');
INSERT INTO Product VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Product VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Product VALUES ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20');
INSERT INTO Product VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
INSERT INTO Product VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20');
INSERT INTO Product VALUES ('0007', '擦菜板', '厨房用具', 880, 790, '2008-04-28');
INSERT INTO Product VALUES ('0008', '圆珠笔', '办公用品', 100, NULL,'2009-11-11');
COMMIT;
```

结尾必须以COMMIT确定才会提交。

* 变更表名

```mysql
RENAME TABLE <原表名> to <新表名>;
```

## 2. 查询基础

### 2.1 SELECT语句基础

* 基础

```mysql
SELECT <列名1>, <列名2>,……
FROM <表名>;
```

例如，从Product表中输出3列：

```sql
SELECT product_id, product_name, purchase_price
FROM Product;
```

* 查询所有列

```sql
SELECT * FROM <表名>;
```

星号（*）表示所有列的意思，列的显示顺序按照定义时的顺序进行排序。

* 为列设定别名

```sql
SELECT product_id AS id,
       product_name AS name,
       purchase_price AS price
FROM Product;
```

使用`AS`关键字为列设定别名。别名可以使用中文，但需要以**双引号（""）**括起来。

```sql
SELECT product_id AS "商品编号",
       product_name AS "商品名称",
       purchase_price AS "商品价格"
FROM Product;
```

* 常数查询

```sql
SELECT '商品' AS string, 38 AS number, '2009-02-24' AS date,
       product_id, product_name
FROM Product;
```

所有的行中都显示出了 SELECT 子句中的常数。

* 从结果中删除重复行

```sql
SELECT DISTINCT product_type
FROM Product;
```

通过SELECT子句中使用`DISTINCT`关键字实现。**DISTINCT关键字只能用在第一个列名之前**。

**注意：NULL值也会作为一列数据**

* 根据WHERE语句选择记录

```sql
SELECT <列名>, ……
FROM <表名>
WHERE <条件表达式>;
```

**注意：SQL中子句书写是固定的。**

### 2.2 算数运算符与比较运算符

* 在语句中进行四则运算

```sql
SELECT product_name, sale_price,
       sale_price * 2 AS "sale_price_x2"
FROM Product;
```

* 比较运算

```sql
SELECT product_name, product_type
FROM Product
WHERE sale_price <> 500;
```

**注意：不等于用`<>`表示。**

**注意：不能对NULL进行比较运算，如果需要选取是应运用`IS NULL`或`IS NOT NULL`运算符**

```sql
SELECT product_name, purchase_price
FROM Product
WHERE purchase_price IS NULL;
```

### 2.3 逻辑运算符

* NOT运算符

NOT不能单独使用，必须和其他查询条件组合使用，表示否定。

* AND运算符和OR运算符

对多割查询条件进行组合。

**注意：AND运算符优先于OR运算符**

* 三值逻辑

当记录单元格中存放为NULL时，进行逻辑比较会出现UNKONWN（不确定）的情况。

## 3. 聚合与排序

### 3.1 聚合查询

* 聚合函数

COUNT： 计算表中的记录数（行数）
SUM： 计算表中数值列中数据的合计值
AVG： 计算表中数值列中数据的平均值
MAX： 求出表中任意列中数据的最大值
MIN： 求出表中任意列中数据的最小值  

```sql
SELECT COUNT(*)
FROM Product;
```

COUNT函数的结果根据参数的不同而不同。 COUNT(*)会得到包含NULL的数据 行数，而COUNT(<列名>)会得到NULL之外的数据行数。

* 计算合计值

```sql
SELECT SUM(sale_price), SUM(purchase_price)
FROM Product;
```

对于 SUM 函数来说，即使包含 NULL，也可以计算出合计值。（所有聚合函数如果以列名为参数，在计算之前会把NULL值排除在外）

* 计算平均值

```sql
SELECT AVG(sale_price)
FROM Product;
```

* 计算最大/最小值

```sql
SELECT MAX(sale_price), MIN(purchase_price)
FROM Product;
```

MAX/MIN函数几乎适用于所有数据类型的列。 SUM/AVG函数只适用于数值类型的列。  

* 删除重复值（DISTINCT）

```sql
SELECT COUNT(DISTINCT product_type)
FROM Product;
```

### 3.2 对表进行分组

* GROUP BY子句

```sql
SELECT <列名1>, <列名2>, <列名3>, ……
FROM <表名>
GROUP BY <列名1>, <列名2>, <列名3>, ……;
```

GROUP BY 子句的书写位置也有严格要求，一定要写在FROM 语句之后（如果有 WHERE 子句的话需要写在 WHERE 子句之后）。  

**注意：使用GROUP BY子句时， SELECT子句中不能出现聚合键之外的列名。**

### 3.3 聚合结果指定条件

* HAVING子句

```
SELECT <列名1>, <列名2>, <列名3>, ……
FROM <表名>
GROUP BY <列名1>, <列名2>, <列名3>, ……
HAVING <分组结果对应的条件>
```

### 3.4 查询结果排序

* ORDER BY子句

```sql
SELECT <列名1>, <列名2>, <列名3>, ……
FROM <表名>
ORDER BY <排序基准列1>, <排序基准列2>, ……
```

**注意：ORDER BY子句通常写在SELECT语句的末尾，默认升序。**

* 指定升序或降序

```sql
SELECT product_id, product_name, sale_price, purchase_price
FROM Product
ORDER BY sale_price DESC;
```

降序关键字DESC，升序关键字ASC，在ORDER BY后使用

* 可以在ORDER BY中使用别名

```sql
SELECT product_id AS id, product_name, sale_price AS sp, purchase_price
FROM Product
ORDER BY sp, id;
```

**注意：一定要记住 SELECT 子句的执行顺序在 GROUP BY 子句之后， ORDER BY 子句之前。  **

* ORDER BY中可以使用的列

在ORDER BY子句中可以使用SELECT子句中未使用的列和聚合函数。

## 4. 数据更新

### 4.1 数据的插入（INSERT）

* INSERT基本语法

```sql
INSERT INTO <表名> (列1, 列2, 列3, ……) VALUES (值1, 值2, 值3, ……);  
```

**注意：对表进行全列 INSERT 时，可以省略表名后的列清单。这时 VALUES子句的值会默认按照从左到右的顺序赋给每一列。**  

**注意：插入NULL值的列不能设置成NOT NULL约束。**

* 插入默认值

在创建表CREATE TABLE时使用了DEFAULT约束来设定默认值。此时可以在VALUES子句中指定DEFAULT关键字。

```sql
INSERT INTO ProductIns 
(product_id, product_name, product_type, sale_price, purchase_price, regist_date) 
VALUES ('0007', '擦菜板', '厨房用具', DEFAULT, 790, '2009-04-28');
```

设置默认值的列，在插入时也可以省略该列，系统会自动赋值。（没有默认值会设定为NULL）

* 从其他表中复制数据：INSERT ... SELECT语句

```sql
-- 将商品表中的数据复制到商品复制表中
INSERT INTO ProductCopy (product_id, product_name, product_type, sale_price, purchase_price, regist_date)
SELECT product_id, product_name, product_type, sale_price, purchase_price, regist_date
FROM Product;
```

**注意：INSERT语句的SELECT语句中，可以使用WHERE子句或者GROUP BY子句等任 何SQL语法（但使用ORDER BY子句并不会产生任何效果）。**

### 4.2 数据删除（DELETE）

* DROP TABLE和DELETE语句

**DROP TABLE**可以将表完全删除，**DELETE**会留下表而删除表中的全部数据。

* DELETE基本语法

```sql
DELETE FROM <表名>;
```

* 指定删除对象

```sql
DELETE FROM <表名>
WHERE <条件>;
```

### 4.3 数据更新（UPDATE）

* UPDATE基本语法

```sql
UPDATE <表名>
SET <列名> = <表达式>;
```

* 指定条件UPDATE

```sql
UPDATE <表名>
SET <列名> = <表达式>
WHERE <条件>;
```

例如：

```sql
UPDATE Product
SET sale_price = sale_price * 10
WHERE product_type = '厨房用具';
```

* 更新为NULL

```sql
UPDATE Product
SET regist_date = NULL
WHERE product_id = '0008';
```

**注意：使用UPDATE语句可以将值清空为NULL（但只限于未设置NOT NULL约束的列）**。

### 4.4 事务

* 创建TRANSACTION

```
事务开始语句;
DML语句①;
DML语句②;
DML语句③;
.
.
.
事务结束语句（COMMIT或者ROLLBACK）;
```

使用事务开始语句和事务结束语句，将一系列 DML 语句（INSERT/UPDATE/DELETE 语句）括起来，就实现了一个事务处理。  

例如：

```sql
-- MySQL事务开始语句
START TRANSACTION;
-- 将运动T恤的销售单价降低1000日元
UPDATE Product
SET sale_price = sale_price - 1000
WHERE product_name = '运动T恤';
-- 将T恤衫的销售单价上浮1000日元
UPDATE Product
SET sale_price = sale_price + 1000
WHERE product_name = 'T恤衫';
COMMIT;
```

## 5. 复杂查询

