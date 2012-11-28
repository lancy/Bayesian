# Bayesian Filtering
## About
贝叶斯过滤算法是一种基于统计学的过滤算法，它使用贝叶斯分类来进行特定类别文本的判别和过滤。
## Naive Bayes classifier
朴素贝叶斯分类器是一种应用基于独立假设的贝叶斯定理的简单概率分类器，这种潜在的概率模型称为独立特性原型。
简单的说，朴素贝叶斯分类器假设样本的每个特征都是独立的与其他特征不相关的，尽管这些特征可能存在相互依赖，或者一些特征由其他特征而决定。
### 概率模型（源自贝叶斯定理）
#### 公式
公式一
**Pr(H | T) = Pr(T | H)·Pr(H) / [Pr(T | H)·Pr(H) + Pr(T | M)·Pr(M)]**

其中:

* Pr(H | T)代表当一条文本有token T存在的时候，命中指定类别文本的概率
* Pr(H)代表对于任意一条文本，命中指定类别文本的概率
* Pr(T | H)代表token T出现在命中指定类别文本中的概率
* Pr(M)代表对于任意一条文本，非命中指定类别文本的概率
* Pr(W | H)代表token T出现在非命中指定类别文本重的概率

通常情况下，我们会假定Pr(H) = Pr(M) = 0.5，即普遍命中概率和普遍非命中概率相等，这种假定是因为我们不想对出现的文本产生偏见关注。在这个假定下，我们可以将公式化简为：

公式一（简）
**Pr(H | T) = Pr(T | H) / [Pr(T | H) + Pr( T | M)]**

#### 合并独立概率
朴素贝叶斯分类器假定每个特征（该应用中为token）都是独立的，则我们可以使用合并概率公式：

公示二
**P = P1·P2···Pn / [P1·P2···Pn + (1 - P1)(1 - P2)···(1 - Pn)]**

其中：
 
* P 即为该文本命中指定类别文本的概率
* Pi (i = 1..n)当文本中出现某一token i，的时候，该文本命中指定类别文本的概率。（上面的Pr(H | T)）

## 实现案例——贝叶斯过滤算法在抽奖微博识别的应用
### 功能
鉴别给定的微博，判断其是否为抽奖微博，从而为后续操作，比如过滤或者自动参与抽奖，提供基础。

### 程序设计
1. 首先收集一定数量的抽奖微博和非抽奖微博，存在不同的两个文件（hitFileName.txt; misFileName.txt）
2. 将两个文件分别读入两个List（hitStringList, misStringList）
3. 对List里的每个string，进行tokenization，并加到对应的两个countTable(dict)，（hitCountTable, misCountTable），countTable用于统计每个token出现的次数。
    * 例：hitCountTable[token]表示token在命中文本中出现的次数）
4. 将countTable转换为对应的probabilityTable，（hitProbabilityTable, misProbabilityTable）:单个token出现的次数 / 整个表所有token出现的次数）
    * 例：hitProbabilityTable[token]表示token在命中文本重出现的概率
5. 用公式一，由hitProbabilityTable和misProbabilityTable求得tokensProbabilityTable
    * tokensProbabilityTable[token]表示当一条文本有token存在的时候，命中指定类别文本的概率
6. 由给定string，分词后，找出它们其在tokensProbabilityTable的概率，用公式二，既可以求出该文本命中指定类型文本的概率

### 代码
代码在Github开源托管[传送门](https://github.com/lancy/Bayesian)

## Contact Me
* [Follow my github](https://github.com/lancy)
* [Follow my weibo](http://weibo.com/lancy1014)
* [Write an issue](https://github.com/lancy/Bayesian/issues)
* Send Email to me: lancy1014@gmail.com