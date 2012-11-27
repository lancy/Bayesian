#encoding=utf-8

#
# hitHash and misHash
# P(A|ti）= P2(ti) / [(P1(ti) + P2(ti)]
#
# probabilityHahs
# P(A|t1, t2, t3 ... tn) = (P1 * P2 * ... * PN) / [P1 * P2 * ... * PN + (1 - P1) * (1 - P2) * ... * (1 - PN)]

import jieba


def tokensFromString(string):
    return list(jieba.cut(string, cut_all=False))


def addTokensToCountTable(tokens, countTable):
    for token in tokens:
        temp = token.encode("UTF-8", errors="strict")
        countTable[temp] = 1


def totalCountFromCountTable(countTable):
    totalCount = 0
    for key in countTable:
        totalCount += countTable[key]
    return totalCount


def probabilityTableFromCountTable(countTable):
    totalCount = totalCountFromCountTable(countTable)
    probabilityTable = dict()
    for key in countTable:
        probabilityTable[key] = countTable[key] / float(totalCount)
    return probabilityTable


def tokensProbabilityTableFromHitAndMisProbabilityTable(hitProbabilityTable, misProbabilityTable):
    probabilityTable = dict()
    for key in hitProbabilityTable:
        if key in misProbabilityTable:
            probabilityTable[key] = hitProbabilityTable[key] / (hitProbabilityTable[key] + misProbabilityTable[key])
        else:
            probabilityTable[key] = 1

    for key in misProbabilityTable:
        if not key in hitProbabilityTable:
            probabilityTable[key] = 0
    return probabilityTable


def probabilityListFromTokensAndTokensProbabilityTable(tokens, tokensProbabilityTable):
    probabilityList = list()
    for token in tokens:
        if token in tokensProbabilityTable:
            probabilityList.append(tokensProbabilityTable[token])
    return probabilityList


def eventProbabilityFromStringAndTokensProbabilityTable(string, tokensProbabilityTable):
    tokens = tokensFromString(string)
    probabilityList = probabilityListFromTokensAndTokensProbabilityTable(tokens, tokensProbabilityTable)
    A = 1
    B = 1
    for probability in probabilityList:
        A = A * probability
        B = B * (1 - probability)
    if A + B == 0:
        return 0
    else:
        return A / (A + B)


hitStringList = [
    "#你转我就送#之《团队正能量》！优秀者拥有正能量，领导者传递正能量，积极团队升华正能量，不能传递的正能量必定会消失，新书《团队正能量——带队伍就是带人心》，助你实现从个人正能量到团队正能量的完美进化！关注@凤凰读书 并转发微博，即有机会获赠，共十本。12月4日截止。",
    "题海战术也要讲方向！即日起至11月30日，广东地区高考党只要关注@优知库 、原文转发本文并@ 三位童鞋，即有机会获赠《试题调研》七彩梦想系列任选三册！放出名额30个，快递寄出，参与从速啦！ http://t.cn/zjqqMJk",
    "“号外号外”江门首家自拍照相馆---ISNAP专业自拍俱乐部即将横空登场与公众见面啦，现在只要你动动手关注并转发该微博，开业当日到店即可获得小礼品一份，并还有机会获赠专业自拍体验1小时消费券（随机抽取名额30个）。更多新奇刺激的玩法尽在 @ISNAP爱拍照自拍照相馆",
    "#辣团网有奖转发活动开始# 1关注辣团网 2转发此条微博并@三个好友就有机会获得下列给力奖品 我们会在12.4抽取三等奖12.10抽取二等奖12.16抽取一等奖 所有参与活动的朋友均可获得台湾第一热销品牌我的心机面膜#辣团独家团#资格http://t.cn/zlFyoQS 心动不如行动 还在等什么 动动手指转发下 大奖等你拿",
    "#心动社联#【华工社团联合会13岁啦】快快来领票和我们一起见证它的成长吧！派票地点：北一北二西区饭堂门前；时间：本周三周四，上午11:30-12:30，下午4:45-6:00关注@广州市力动文化活动策划有限公司 并转发微博，于领票时出示微博凭证即可获得精美雨伞、精美文件夹和精美扇子三样礼品哟",
    "#京东沙漠风暴 优购网上鞋城同贺# 京东商城优购官方旗舰店百丽、他她、天美意、思加图、森达时尚男女鞋2.4折起；Nike、Adidas、CAT等运动户外品牌5.8折起，还有更多惊喜狂点 http://t.cn/zlFXm1V 即日起，关注@优购网上鞋城 转发此微博并@ 2位好友，即有机会获得新款鞋服！",
    "花瓣网：#有奖转发#给力大回馈，花小瓣送您白色iPad mini啦！活动规则很简单,只需 ①关注@花瓣网②转发本活动，就有机会获得一台白色iPad mini，新浪官方活动平台保证绝对公平，拼人品的时候到啦，快行动吧！转起来！！http://t.cn/zjqG92I",
    "为庆祝#OCS灿瑞半导体# 微博正式使用，有奖关注并转发活动。 活动时间：11/15-12/12 活动规则： 1、关注@OCS灿瑞半导体 2、转发本微博并@3位好友 将在每周四抽取5位幸运博友并公布名单，获得移动手机充值卡200元大奖。 活动持续中…",
]

misStringList = [
    "【晚安】有时候或许该想想：你真的是活了一万多天，还是只活了一天，却重复了一万多次？",
    "太阳新天地~ 吃好吃的+看电影。PS:“少年派的奇幻漂流”的自然画面是最有美感的！！",
    "「华丽丽咖啡桌的创意设计」用亚克力制作的透明彩色几何球体堆叠出来的小桌，在阳光照射之后好比贵妇手中的钻石戒指，除了需要担心走路不小心踢到脚趾的后果之外，完全就是个沉迷梦幻逸品！你敢不敢使用这款钻石光咖啡桌，华丽的享受一次奢侈的饮咖时光吧！",
    "呜呜呜呜，好冷啊这个天气还用凉席和空调被的人活该被冻到睡不着",
    "赞，本来只是想试着写一下人工智能大作业bayesian，结果，结果，结果居然一下就写完了。。",
    "18天。即使深夜也不再被负能量包围。今年的冬天比想象中要冷，但是却教会我去热爱这个世界。The whole world is waiting for u！Hold out，girl！",
    "疯狂转发中！首次担纲制片人，希望各位捧场！//@吴奇隆: 孩子們瘋狂轉發吧！◆◆@新浪娱乐：【《明星Do in Style》首播 吴奇隆型男教学】新节目千呼万唤终于来啦~~~他是万人偶像“霹雳虎”，是内敛专情“皇四爷”，是最潮土匪“疯子雷”!#明星Do in Style#首期嘉宾@吴奇隆特别准备了独家型男教学。看吴奇隆如何翻转世界，教你一秒变型男！ 观看完整节目：http://t.cn/zjqAYt0",
    "#第二届e.bm校园营销挑战赛#复试名单公布恭喜以下团队晋级复赛！请晋级的团队继续完成课题方案并在规定时间内上传完整的营销方案，了解详情请登陆大赛官网http://t.cn/zlFYYsj@周大福ebm导师团",
    "#Boogie！Boogie！HIPHOP文化月#HIPHOP文化中，Boogie意为随着音乐摆动身体。Boogie是每个人的权利，在中大，无论在公教或是食堂，听到音乐就可以动起来！接下来的30天，我们将全力打造属于中大的HIPHOP文化月！最权威的文化讲座，最free的Dance party，最炸的舞会表演，你岂能错过？Let SYSU boogie！",
    "刘德生生不息生机勃勃：碉堡。。//@BBBBBehahn在中大混碗饭吃: 学毛，直接长跪不起。。。//@蓝色蝶殇_混碗饭吃: 我日，你要不要学一学@BBBBBehahn在中大混碗饭吃//@RedDevils-7-泽钦: 温格表示要收购了//@创造与成功_何朔水: 我擦！！！这人卖艺浪费了！！！来恒大吧！@RedDevils-7-泽钦◆◆@虎扑足球：#虎扑视频#从没见过的神级控球！给外国牛人跪了！（摘选评论：玩到极限了；真正的人球合一；太尼玛牛叉了，技巧，力量的完美结合；这个领域他就是梅西……；#巴神跑到街头卖艺了？#我不行了……看得鸡皮疙瘩都起来了；杂耍中足球玩得最好的，玩足球中杂耍最好的！",
    "感谢康先生康太太关注并转发。安拉给每个人不同的尔林，我们用它来传播主道。康太太帮助汉族穆斯林姐妹，一样是传播了伊斯兰的光辉。祈求伟大的安拉慈敏康先生康太太，愿两位身体健康，愿康先生艺术生命常青！ //@相声演员康松广:回复@冰岛中文:学习并转发了，是与老伴一起看的。有个跟老伴学礼拜的女",
    "梓纯桑：@_市隐@Tata_紫涵@立立程@小切猫咪会变成那个人//@大学城周sir://@广东工业大学机电学生会: 【身体是革命的本钱】大家都尽量不要熬夜，注意休息啊！◆◆@南有乔木229：据悉，我校信息学院10级陈某同学昨晚入睡后，今天（11月27日）早上7点多舍友发现叫其不醒，马上打120、110，医生第一时间赶到现场抢救至8点38分宣告不治。医生与法医鉴定其为猝死。在此深表痛惜与哀悼！",
]


hitCountTable = dict()
for hitString in hitStringList:
    addTokensToCountTable(tokensFromString(hitString), hitCountTable)
hitProbabilityTable = probabilityTableFromCountTable(hitCountTable)

misCountTable = dict()
for misString in misStringList:
    addTokensToCountTable(tokensFromString(misString), misCountTable)
misProbabilityTable = probabilityTableFromCountTable(misCountTable)

tokensProbabilityTable = tokensProbabilityTableFromHitAndMisProbabilityTable(hitProbabilityTable, misProbabilityTable)


testStringList = [



]


for x in range(0, len(testStringList)):
    print "Test", x, "probability =", eventProbabilityFromStringAndTokensProbabilityTable(testStringList[x], tokensProbabilityTable)
