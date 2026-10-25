# -*- coding: utf-8 -*-
"""生成 works.html 著作网格与 works/*.html 详情页。
数据集中在本文件 WORKS 列表，新增/修订著作只需改这里再运行：
  python3 tools/build_works.py
"""
import os
import re
import json

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------- 数据
WORKS = [
    dict(
        title="一般法理学", role="著", year="2026",
        slug="yiban-falixue", cover="yiban-falixue.jpg",
        tags="法理学",
        meta=[
            ("作者", "赵英男"),
            ("出版社", "北京大学出版社"),
            ("出版时间", "2026 年 1 月"),
            ("丛书", "法律人进阶丛书 · 法学拓展（李昊 主编）"),
            ("ISBN", "978-7-301-36996-8"),
            ("页数 / 定价", "366 页 / 88.00 元"),
        ],
        intro="本书是有关现代法理学传统理论和前沿进展的导论性著作。聚焦于法律概念和司法裁判，本书探讨了法律实证主义、自然法、取消主义、法律现实主义以及规则与案例的一般理论，围绕“法律是什么”“为何遵循法律”“法官如何裁判”等问题展开阐释。全书共十二章，分为总论、法律概念、司法裁判三个部分，在评析不同理论观点的基础上，试图阐明理论思考的一般方法与建构法律理论的可行路径：既是初学者了解法理学的入门著作，也可以作为深入研究法理学的进阶参考。本书受“同济大学研究生教材建设项目”（2025JC33）资助。",
        afterword_title="后记",
        afterword="「待补」本书后记全文将由作者确认后补入。",
        afterword_note="目录显示本书末有后记，网上未见全文。",
        links=[],
    ),
    dict(
        title="企鹅哲学史（全两册）", role="译", year="2023",
        slug="qi-e-zhexueshi", cover="qi-e-zhexueshi.jpg",
        tags="哲学史",
        meta=[
            ("作者", "[英] A.C. 格雷林"),
            ("译者", "赵英男、张瀚天"),
            ("出版社", "上海文艺出版社"),
            ("出版时间", "2023 年 1 月"),
            ("ISBN", "978-7-5321-8183-4"),
            ("页数 / 定价", "756 页 / 128.00 元"),
        ],
        intro="《企鹅哲学史》是英国哲学家 A.C. 格雷林追步罗素《西方哲学史》而完成的哲学通史。上卷以前苏格拉底哲学家为起点，穿行古希腊、中世纪、文艺复兴与启蒙时代，止于尼采、布拉德雷与杜威；下卷书写 19 世纪末之后的哲学，按分析哲学与欧陆哲学分庭抗礼的态势平行展开。全书涵盖知识论、形而上学、伦理学、美学、逻辑学、心灵哲学等领域，并将印度、中国、阿拉伯—波斯以及非洲的哲学传统纳入视野。2023 年入选“世纪好书”1 月榜与 3 月文学报好书榜。",
        afterword_title="译后记",
        afterword="「待补」本书译后记全文将由译者确认后补入。",
        afterword_note="目录显示本书末有译后记；豆瓣与公众号未见全文。",
        links=[("豆瓣 · 企鹅哲学史", "https://book.douban.com/subject/36165941/")],
    ),
    dict(
        title="法理学：主题与概念（第三版）", role="译", year="2023",
        slug="falixue-zhuti-yu-gainian", cover="falixue-zhuti-yu-gainian.jpg",
        tags="法理学 · 教科书",
        meta=[
            ("作者", "[英] 斯科特·维奇、[希腊] 埃米利奥斯·克里斯多利迪斯、[意] 马尔科·哥尔多尼"),
            ("译者", "赵英男"),
            ("出版社", "北京大学出版社"),
            ("出版时间", "2023 年 1 月"),
            ("丛书", "法律人进阶译丛"),
            ("ISBN", "978-7-301-33635-9"),
            ("页数 / 定价", "386 页 / 69.00 元"),
            ("原书", "Jurisprudence: Themes and Concepts, 3rd ed., Routledge, 2018"),
        ],
        intro="本书为法理学课程研习的核心主题提供了富有原创性的导论与批判性分析。第一部分讨论法律与现代性；第二部分讨论法律体系与法律推理，涵盖法治、合法性、权力、法律实证主义、自然法、法与道德、法律解释和法律推理等十个传统核心议题；第三部分聚焦正义学说、全球正义、转型正义、法律多元主义、司法化与法律自创生等高阶话题。本书将哲学、社会学、政治（哲）学要素有机结合，从多角度推进而非仅仅介绍既有研究。",
        afterword_title="译者序（代译序）",
        afterword=(
            "法理学是法学十六门基础课之一，却是比较独特的一个。相较于民法、刑法、宪法以及行政法等科目，法理学的学科体系并不围绕特定实在法展开，学科理论也不以注释和解读法律规范为核心内容……如此学科特质使得法理学呈现出千变万化的样态，“有多少人讲授法理学，就有多少种法理学”可能并非夸张，而是对法理学这门学科发展现状的如实描述。"
            "<br><br>法理学是法学十六门基础课之一……它的存在让我们有关法律的研究不再局限于实在法，而是将经济学、社会学、政治哲学、伦理学等更广阔的视角纳入法学视野。但利之所在，往往弊亦随之。学理体系的开放，有时候反而不利于形成学科共识：在教学与研究中，老师难教、学生难学、学者间难对话的情况数见不鲜；不以实在法为依归的研究进路，往往不利于具体司法实践问题的解决，法理学理论难用甚至无用的观点可以说不绝于耳。……"
            "<br><br>出现在读者面前的这部作品，就是从教科书层面革新法理学的一次尝试，自 2007 年初版至今已历经三版。坦率地说，在当下，国内学者的作品以及对英、美、德、日等国学者作品的译介其实已经使法理学教材市场日趋饱和。我们为什么还需要引进一本法理学教材？这要从法理学的学科特质，学习、讲授特点，课程存在的问题以及本书的特征谈起。……"
        ),
        afterword_note="节选自译者序《追寻法理学的另一种可能》（燕大元照公众号刊出）。另有译者长文书评《站在哈特的延长线上》刊于澎湃新闻。",
        links=[
            ("译者序全文（燕大元照）", "https://mp.weixin.qq.com/s?__biz=Mzg3Mzk3NDQ1NA==&mid=2247486424&idx=2&sn=859ffc82e11cef614ec5ab161c3eeea2"),
            ("译者书评《站在哈特的延长线上》（澎湃新闻）", "https://m.thepaper.cn/newsDetail_forward_21393038"),
        ],
    ),
    dict(
        title="法律多元主义阐释：历史、理论与影响", role="译", year="2023",
        slug="falv-duoyuan-zhuyi", cover="falv-duoyuan-zhuyi.jpg",
        tags="法律多元主义 · 法理学",
        meta=[
            ("作者", "[美] 布莱恩·Z. 塔玛纳哈"),
            ("译者", "赵英男"),
            ("出版社", "商务印书馆"),
            ("出版时间", "2023 年 3 月"),
            ("丛书", "法政名著译丛（精装）"),
            ("ISBN", "978-7-100-21769-9"),
            ("页数 / 定价", "368 页 / 85.00 元"),
            ("原书", "Legal Pluralism Explained, Oxford University Press, 2021"),
        ],
        intro="本书是塔玛纳哈有关法律多元主义以及法哲学三十余年研究的集大成之作。法律多元主义涉及国家法、国际法、跨国法、习惯法、宗教法、原住民法等多重法律形态的彼此共存。本书依赖有关中世纪、奥斯曼帝国、后殖民社会、原住民族、犹太教与伊斯兰教法以及西方国家法律体系的研究，表明“国家拥有统一法律体系并垄断法律”的主导观点一直以来都是错漏百出的；并通过作者提出的“惯习主义”方法，既克服了法律多元主义方法论上的困难，也批判了当代法哲学主流学说的空洞。豆瓣评分 8.8。",
        afterword_title="译后记",
        afterword="「待补」本书译后记全文将由译者确认后补入。",
        afterword_note="目录显示本书末有译后记（“法律是什么：塔玛纳哈的回答”附录后）；网上未见全文。",
        links=[
            ("商务印书馆官方页", "https://www.cp.com.cn/book/6afe7328-a.html"),
        ],
    ),
    dict(
        title="语境中的法学家：威廉·特文宁学术回忆录", role="译", year="2024",
        slug="yujing-zhong-de-faxuejia", cover="yujing-zhong-de-faxuejia.jpg",
        tags="法理学 · 回忆录",
        meta=[
            ("作者", "[英] 威廉·特文宁（William Twining）"),
            ("译者", "赵英男"),
            ("出版社", "商务印书馆"),
            ("出版时间", "2024 年 7 月"),
            ("丛书", "法政名著译丛（精装）"),
            ("ISBN", "978-7-100-23623-2"),
            ("页数 / 定价", "734 页 / 145.00 元"),
            ("原书", "Jurist in Context: A Memoir, 2019"),
        ],
        intro="本书是英国杰出法学家威廉·特文宁以切身经历为线索，对 20 世纪 50 年代以来法理学发展历程的回顾与展望。它既是一部引人入胜且通俗易懂的学术回忆录，讲述了特文宁的思想与著述在非洲、北美洲以及欧洲的语境中长达六十余年的发展；又是一部严肃而权威的法学理论专著，探讨了法律的概念、法律教义、法律推理、语境中的法律、法律与发展、法律现实主义、法律多元主义、法学教育、重新思考证据、法律与全球化等议题。",
        afterword_title="译后记（节选）",
        afterword=(
            "……当我读到 1964 年 30 岁的特文宁教授在非洲乞力马扎罗山、在对未来充满困惑与犹疑中做出人生选择时，我仿佛看到了自己以及周围朋友的境况与模样。吴婧老师细致热忱的帮助以及丛书主编田雷老师一如既往的支持，使得我与本书的缘分越来越近。在与特文宁教授联络后，我更笃定自己的眼光与选择是正确的。老人家的幽默坦诚和细致敏锐，可以说与我阅读他的著作时心中所设想的那个形象别无二致。同样感谢布莱恩·Z. 塔玛纳哈教授，他不仅推荐我阅读特文宁教授的作品，还亲自将自己写作的相关短文扫描后发送给我。"
            "<br><br>本书的翻译工作虽然辛苦却相当顺利。为了应对这个原书将近四百页的“大部头”，我在两个月的时间内几乎每天都争取在凌晨 5 点起床，上午 7 点前开始工作。考虑到本书内容有很强的“语境性”，我在翻译完毕后的校对过程中，针对学术概念、历史事件、文化背景等内容补充了许多（或许太多？）译者注释。它们都以页下脚注形式出现，以区别于作者本人在正文后的详细引注。这是特文宁教授的建议。他说这本书所带来的翻译挑战“可能更多是文化性的而非语义性的”。确实如此！……我希望自己的这番尝试无损于本书的严肃、权威与含蓄，更希望以此能够推动我与特文宁教授共享的一个目标：读者为了寻找有关卢埃林、哈特以及德沃金等人的八卦而翻开本书，但在合上书后却对法理学有了一番截然不同的理解。"
            "<br><br>译事艰辛，并非今日始知。翻译一个词或一句话很简单，但翻译一整部书就像是一个人走路，走的多了不免歪歪扭扭甚至错漏百出。身为译者，我由衷感谢读者诸君的热情支持，也诚恳期盼各位贤达的讨论指正！"
            "<br><br>—— 赵英男，2023 年 1 月 25 日"
        ),
        afterword_note="节选自译后记《“把自己作为方法”：如何阅读〈语境中的法学家〉》（豆瓣书评页刊出），全文待补。",
        links=[("商务印书馆官方页", "https://www.cp.com.cn/book/e1d9b4cb-f.html")],
    ),
    dict(
        title="自然化法学：美国法律现实主义和法哲学中的自然主义文集", role="译", year="2024",
        slug="ziranhua-falixue", cover="ziranhua-falixue.jpg",
        tags="法律现实主义 · 法理学",
        meta=[
            ("作者", "[美] 布莱恩·莱特（Brian Leiter）"),
            ("译者", "赵英男"),
            ("出版社", "商务印书馆"),
            ("出版时间", "2024 年 11 月"),
            ("丛书", "法哲学名著译丛（精装）"),
            ("ISBN", "978-7-100-23512-9"),
            ("页数", "494 页"),
            ("原书", "Naturalizing Jurisprudence"),
        ],
        intro="布莱恩·莱特是美国法律现实主义的杰出哲学阐述者，也是法理学议题自然主义转向的核心人物。《自然化法学》汇集了莱特在此领域得到广泛关注的重要作品，并补充了他为此书专门撰写的长篇导言与两篇后记，是莱特在法理学领域得到公认的代表作。文集涵盖一般法理学、司法裁判、法律现实主义、奎因自然主义哲学、法律与道德客观性以及哈特—德沃金之争等议题。",
        afterword_title="译后记（全文）",
        afterword=(
            "从未想过一本书的翻译会持续 6 年之久。最早有意引进本书是在 2017 年。当时我正在北京大学法学院读书，申请了国家留学基金管理委员会的奖学金，远赴美国圣路易斯华盛顿大学跟随布莱恩·Z. 塔玛纳哈教授访学一年。在他的影响下，我逐渐认识到法律现实主义（Legal Realism）虽然不过是美国法学发展史中的一种“历史现象”，但却对今时今日的美国法学乃至世界法学思潮与司法制度运作发挥着不可忽视的作用。通过阅读他的著作，我开始留意与他同时代的学者及其前辈们有关法律现实主义的论述。布莱恩·莱特教授的《自然化法学》自然成为我的重要参考。通读此书两遍后，我便联系当时刚刚进入中国政法大学比较法学研究院工作的我的师兄孙海波，希望一同翻译引进这部著作。"
            "<br><br>当然，说是“一同翻译”，我实际上是希望依靠着师兄的经验与能力“在大树底下好乘凉”。不过后来我们的学习与工作计划几经变动，翻译进度与安排也随之调整延宕，原本联系好的出版社又难免出现变数。我甚至一度以为，自己完成的本书第 4 章到第 9 章的译稿或许只能静静地等在电脑硬盘里，成为我可能发表又可能“敝帚自珍”的一篇篇论文的灵感来源或注释说明。但幸运的是，吴彦老师伸出援手，不仅慷慨应允纳入译丛，还向商务印书馆大力举荐引进。当我在 2022 年 11 月底得到消息，可以整理译稿准备提交时，一瞬间我想到的竟然不是感谢，而是马克斯·韦伯在《以政治为业》结尾所说的一句话：政治是件用力而缓慢穿透硬木板的工作，它同时需要激情和眼光。这句话中的“政治”改换成“学术”或任何一件事，都是成立的。我们的世界的确如韦伯所说，除非我们执着地寻觅这个世界上的不可能之事，否则可能之事皆不可得。既然有了好消息，那就行动起来！"
            "<br><br>将近 6 年的时间过去了，海波师兄从讲师成为副教授，但无疑仍属高校体制下的一枚“青椒”。我则一如既往的时间暂有余裕。经过一番权衡商量，我打算独自完成本书翻译。充分利用年来 20 多日的可以静心修养、安心工作的“假期”，我完成了本书剩余部分的译文。在统稿时我本来自信满满，但通读一遍译文后，发现自己多年前的工作确实还有诸多疏漏——对许多原文一知半解，对许多长句拆解有误，就连很多中文表述也是歧义丛生、行文滞涩。这样我就又用了一些时间对照原文，一字一句修理这些“少作”，最终大概有七成左右的内容是经过重新调整、修改以及润色的。这时我才明白“事缓则圆”意味着什么。"
            "<br><br>不过，我在心底仍愿意相信，这本书的主体内容是我在每个天刚蒙蒙亮的早上匆匆吃一口早饭来到圣路易斯华盛顿大学法学院图书馆，又在天色逐渐灰暗法学院内暖人的橘色灯光亮起时心惊胆颤地步行回家这样平平无奇的日子里翻译完成的。"
            "<br><br>最后简单介绍一下本书的作者与术语翻译。……本书《自然化法学》就是他在该领域的代表作。虽然只是一部文集，但其收录的每篇文章都在法理学讨论中具有举足轻重的地位，特别是他对法律现实主义的自然主义重构以及对“哈特—德沃金之争”的再评价，可以说影响了今时今日人们对于法理学思想资源、理论性质以及方法定位等根本问题的看法。在这个意义上，本书标题译为“自然化法理学”同样是合适的，毕竟书中大部分内容都与法理学直接相关。不过仔细体会莱特的论述就可以发现，本书以法理学为主却不局限于法理学。更准确地说，莱特的构想是系统论述哲学中的自然主义为何以及如何对法学研究有所启发，而法理学不过是他最为熟悉且可用作典型例证的一个领域。基于这个考虑，我利用英语中 jurisprudence 这个词的多义性，将本书标题译为“自然化法学”，试图提醒读者本书不过是一个“论纲”。"
            "<br><br>一部译作的推出，内心总是激动又忐忑。感谢商务印书馆学术中心的编辑以及为之付出的诸位工作人员。我热切地渴望来自诸位读者贤达的反馈与指正！"
        ),
        afterword_note="全文刊于商务印书馆公众号新书推文。",
        links=[
            ("译后记全文（商务印书馆公众号）", "http://mp.weixin.qq.com/s?__biz=Mzk2NDM3NDU0MQ==&mid=2247613416&idx=1&sn=6118187d30ada4f0c729222b1ece3ef8"),
            ("商务印书馆官方页", "https://www.cp.com.cn/book/2abb2033-b.html"),
        ],
    ),
    dict(
        title="掉队的男人：当代男性的现实困境", role="译", year="2024",
        slug="diaodui-de-nanren", cover="diaodui-de-nanren.jpg",
        tags="社会政策 · 性别研究",
        meta=[
            ("作者", "[英] 理查德·V. 里夫斯（Richard V. Reeves）"),
            ("译者", "赵英男"),
            ("出版社", "中国科学技术出版社"),
            ("出版时间", "2024 年 10 月"),
            ("丛书", "雅理 · 中科书院"),
            ("ISBN", "978-7-5236-1102-9"),
            ("页数 / 定价", "362 页 / 79.00 元"),
            ("原书", "Of Boys and Men: Why the Modern Male Is Struggling, Why It Matters, and What to Do about It"),
        ],
        intro="男孩和男人掉队了吗？从小学到大学，无论是成绩还是其他学业表现，男孩似乎越来越落后于女孩；面对经济结构变化，当力量型工作逐渐被人工智能取代，男性岗位首当其冲；当父亲不再是唯一养家糊口的人，他们面临着角色的错位和缺位。本书认为，这不只是男孩和男人遇到的难题，也是需要共同面对的困境：如果男孩可以晚一年入学，如果更多男性能够进入教育、护理等行业，如果父亲角色不再与“供养者”捆绑在一起，将有助于推动真正的性别平等。本书为《纽约时报》年度重要作品、《纽约客》《经济学人》年度图书、奥巴马夏季书单入选。",
        afterword_title="译后记",
        afterword="「待补」本书译后记全文将由译者确认后补入。",
        afterword_note="目录显示本书末有译后记；豆瓣与公众号未见全文。",
        links=[],
    ),
    dict(
        title="法理论的社会学进路", role="译", year="2025",
        slug="falilun-shehuixue-jinlu", cover="falilun-shehuixue-jinlu.jpg",
        tags="法理学 · 社会理论",
        meta=[
            ("作者", "[美] 布莱恩·Z. 塔玛纳哈"),
            ("译者", "赵英男"),
            ("出版社", "北京大学出版社"),
            ("出版时间", "2025 年 1 月"),
            ("ISBN", "978-7-301-35415-5"),
            ("页数 / 定价", "201 页 / 49.00 元"),
            ("原书", "Sociological Approaches to Theories of Law, Cambridge Elements, 2022"),
        ],
        intro="本书原作是剑桥大学出版社“基本原理丛书——法哲学”中的一部。本书运用社会学经典理论与经验素材批判性考察了分析法哲学家围绕“法律是什么”所提出的一系列命题，内容涵盖法律的人造物理论、法律的社会建构理论、法律功能与法律性质、法律体系与生活的脱嵌、法律的指引功能以及社会实效命题等。本书试图表明：分析法哲学无须成为社会学法学，社会科学也无法解决所有关于法律的哲学问题；但两种研究进路可彼此借鉴，有关法律性质的哲学分析应当得到法律运作现实状况的验证和改进。",
        afterword_title="译后记（全文）",
        afterword=(
            "伊塔洛·卡尔维诺在《看不见的城市》中曾虚构了这样一段在忽必烈可汗与马可·波罗之间的对话。彼时两人正在对弈，心中的想法却截然不同。忽必烈可汗认为自己疆域广阔的帝国可以被还原为像棋盘一样由六十四个方格有序排列而成的事物。这种将复杂化约为单一、将现象还原为本质的思路，才是理解世界之道。可是马可·波罗却提醒他说：“陛下，你的棋盘是由乌木和枫木两种木头镶嵌而成的。你现在注视的方格，是一个干旱年份里生长的树干上的一段：你看到它的纤维纹理了吗？这里是勉强可见的一个结节：早春萌生的树芽被夜间一场霜给打坏了。”这似乎意味着任何单一的现象中都蕴藏着无垠的整个宇宙。理解这个世界，就不得不承认以及享受这种复杂乃至失序。"
            "<br><br>类似的情节也出现在余华的笔下。在《河边的错误》中，一个凶手在偏僻荒凉的小镇里大杀四方。经过刑警队长马哲的细致排查，嫌疑人最终被确定为镇里唯一的一个疯子。……认为世间一切行为都有内在逻辑的马哲，便在一丝不苟地探究疯子背后“真相”的过程中一步步陷入了癫狂。这不禁会让我们揣测：或许这个世界本就如此，本就没有我们可以轻而易举掌控的本质、体系以及秩序？我想布莱恩·Z. 塔玛纳哈教授大概会赞同这个推断。在我的理解中，《法理论的社会学进路》讲述的也是这样一个故事。只不过在这里，主人公是执着于探究法律本质必然属性的分析法哲学家，而情节与对话则是一般法理学中有关法律概念、法律功能、法律实效以及法律体系的诸多典型看法。一如卡尔维诺和余华，塔玛纳哈想说，法律作为一种社会制度，在生成、发展、演进与运作的过程中，会受到政治、经济、文化、历史以及社会等各种各样因素的影响。法律的复杂程度不亚于其所从属的生活本身。"
            "<br><br>身为法学家，我们与其寻求将复杂的法律现象在概念上归拢为具有本质必然属性、逻辑严密且有典型特征的事物，倒不如坦率地承认：我们就是永远无法提出一种可以得到所有人认同的界定法律的标准，就是永远无法创立一套不包含任何矛盾与漏洞的法律体系，就是永远无法依靠法律来指引我们日常生活中的绝大多数行为。当然，这不是让我们彻底放弃阐释法律现象的理论努力，也不是愤世嫉俗地轻蔑任何理论范畴的认知意义，而是主张我们应当像马可·波罗那样，观察眼前重要法律现象的生成演变，让理论成为体会世界本身复杂性与多样性的一种方式，而非裁断生活、为之强加逻辑与意义的工具。"
            "<br><br>说回本书作者塔玛纳哈教授。他是我在美国圣路易斯华盛顿大学访学期间的合作导师，回国后我也一直与他保持着联系。我几乎读过他写作的所有著作和论文。有时我会写信向他求教或求助，偶尔他也会把最新写好的文章发过来，请我谈谈看法。2021 年的夏天，他发来一篇长文，在“Word”中足足有 100 页。一年后本书正式出版时，我才知道那便是本书的初稿。……"
            "<br><br>最后简短交代一下本书的翻译。承蒙北京大学出版社与张宁老师的信任，我有机会再次一字一句地整理自己精读塔玛纳哈教授文字后的心得。……翻译无法百分之百地忠实于原作，译文究其实质不过是译者自身学养与能力的告白。我希望自己的文字不会有太多错漏。（引注从略）"
        ),
        afterword_note="全文刊于“法理杂志”公众号。",
        links=[
            ("译后记全文（法理杂志公众号）", "http://mp.weixin.qq.com/s?__biz=Mzk2NDM3NDU0MQ==&mid=2247613496&idx=1&sn=2e1c2749543f87849db0439e7dfa694c"),
        ],
    ),
    dict(
        title="施特劳斯论历史的终结：黑格尔《历史哲学》讲疏", role="译", year="2025",
        slug="shiteliaosi-lishi-zhongjie", cover="shiteliaosi-lishi-zhongjie.jpg",
        tags="政治哲学 · 黑格尔",
        meta=[
            ("作者", "[德] 列奥·施特劳斯 讲疏，保罗·弗朗哥 编"),
            ("译者", "赵英男"),
            ("出版社", "上海文艺出版社"),
            ("出版时间", "2025 年 10 月"),
            ("ISBN", "978-7-5321-9358-5"),
            ("页数 / 定价", "598 页 / 148.00 元"),
            ("原书", "On Hegel, The University of Chicago Press, 2019"),
        ],
        intro="1965 年冬天，列奥·施特劳斯在芝加哥大学开设了一门关于黑格尔的课程。本书重建了这门课程，并在需要之处补充 1958 年课程的记录片段。施特劳斯主要聚焦于《历史哲学》，认为这一讲演录比黑格尔的著作更为易读，且从中能发现其全部政治哲学的历史母体。他在解读黑格尔的过程中，继续推进他一贯的研究，即揭示现代哲学与古代思想的关联，并探讨现代政治理论的发展与局限。本书被视为施特劳斯讲疏整理项目的“收官之作”，书末附有译者附录三篇（黑格尔哲学术语指南、黑格尔年表、课程与出版概况）。",
        afterword_title="译后记",
        afterword="「待补」本书译后记全文将由译者确认后补入。",
        afterword_note="目录显示本书末有译后记（第 588 页起）；网上未见全文。",
        links=[
            ("译者书评《当密涅瓦的猫头鹰在黄昏起飞》（澎湃新闻）", "https://m.thepaper.cn/newsDetail_forward_32111619"),
        ],
    ),
    dict(
        title="法律实用主义研究", role="译", year="2025",
        slug="falv-shiyongzhuyi", cover="falv-shiyongzhuyi.jpg",
        tags="法律实用主义 · 法哲学",
        meta=[
            ("作者", "[美] 迈克尔·沙利文（Michael Sullivan, 1966–2022）"),
            ("译者", "赵英男"),
            ("出版社", "河南大学出版社"),
            ("出版时间", "2025 年 10 月"),
            ("丛书", "实用主义边界译丛（上河文化）"),
            ("ISBN", "978-7-5649-6268-5"),
            ("页数 / 定价", "208 页 / 42.00 元"),
            ("原书", "Legal Pragmatism: Community, Rights, and Democracy, 2007"),
        ],
        intro="本书以清晰简明的文风阐明了实用主义有关权利、共同体以及民主生活的基本立场，为理解医疗、教育、婚姻和政治制度等议题提供了具有现实意义的理论框架。从古典实用主义出发，本书正本清源地回应了德沃金与波斯纳对于实用主义的误解，并将法律实用主义定位为有关现代社会共同生活的反思性与批评性考察，是当代法律实用主义研究的重要作品。",
        afterword_title="译后记",
        afterword="「待补」本书译后记全文将由译者确认后补入。",
        afterword_note="目录显示本书末有译后记；网上未见全文。",
        links=[],
    ),
    dict(
        title="自然法与实践理性", role="译", year="2025",
        slug="ziranfa-yu-shijian-lixing", cover="ziranfa-yu-shijian-lixing.jpg",
        tags="自然法 · 道德哲学",
        meta=[
            ("作者", "[美] 马克·C. 墨菲（Mark C. Murphy）"),
            ("译者", "赵英男"),
            ("出版社", "商务印书馆"),
            ("出版时间", "2025 年 11 月"),
            ("丛书", "自然法名著译丛（精装）"),
            ("ISBN", "978-7-100-25706-0"),
            ("页数 / 定价", "440 页 / 85.00 元"),
            ("原书", "Natural Law and Practical Rationality, Cambridge University Press"),
        ],
        intro="自然法理论近来正历经着一场复兴，在政治哲学和法理学领域中尤为如此。但在最根本的意义上，自然法理论并非政治理论而是道德理论，或者更准确地说，它是一种实践理性理论。自然法立场认为，行动的基本理由是建立在人类本性之上的内在善。本书是对当下有关实践理性的自然法学说的辩护，既展现出其固有的合理性，又同与之竞争的利己主义、后果主义、康德主义以及美德立场展开系统性对话，对道德哲学、法哲学以及政治理论领域的研习者均有启发。",
        afterword_title="译后记（全文）",
        afterword=(
            "2021 年春节过后，吴彦老师邀请我为他在商务印书馆主编的“自然法名著译丛”做些事情。简单商量后，我们决定译介美国乔治城大学马克·C. 墨菲教授的这部《自然法与实践理性》。2022 年 7 月初，本书正式在商务印书馆立项；同年 11 月中旬，我在等待博士后出站与投出求职简历后，重拾译笔着手翻译。那一年的隆冬在我的记忆里呈现为灰蒙蒙的一片。在大概四十天的时间里，我或者无法走出家门，或者无法走出小区，又或者由于高烧和疼痛而需要卧床休息。本书的一半篇幅就是在这种情形下译成的。新闻中的风起云涌，主干道上的空无人烟以及白色的衣服、车辆与帐篷所带来的紧张焦虑，都在墨菲书中难解的论点与拗口的长难句面前消弭于无形。由此，我相信了书写的力量：这是一种以文字形态或隐或显地让人免于遗忘的力量。"
            "<br><br>冬至过后直到春分，北半球的黑夜逐渐不再漫长。我生活与工作的重心也将从北京南迁至沪上。在离开那间暖气余温未消的出租屋前，我在网上下单了一双到上海即可换上的新鞋。鞋子虽新，老路却依旧要走——在我看来，自己的生活与工作其实没有任何变化，只是要在不同的地方写注定要写的东西，要对不同的人说注定要说的话，仅此而已。这样我又在或坦荡或自有款曲的五角场与四平路中完成了本书另一半内容的校译。"
            "<br><br>但实事求是地讲，我还是没有理解本书的核心主旨，也不甚明了墨菲教授为之提供的详细论证。根据我粗浅的理解，本书是一部探讨我们基于何种标准能够判定一种行动是否值得去做的著作。墨菲教授认为，通过一系列理论辨析，我们会发现构成这种判准的理论是一种自然法学说。这指的是该学说主张，构成我们行动根本理由的事物是立基于人类本性的善。墨菲将这些善称为基本善，主要包括生命、知识、审美体验、游戏与工作中的卓越、能动性的卓越、内心平静、友谊与社群、宗教以及幸福九种。讨论和辩护这些基本善的属性，构成了本书的主体内容。……"
            "<br><br>有关这个整体基本立场，我们或许可以重点关注墨菲在以下三方面的论断。第一个论断涉及“我们如何获知基本善”这个问题……这便是“实际同一性命题”。第二个论断涉及“基本善或人类福祉是否具有客观性”这个问题……正是在这个意义上，墨菲认为基本善及人类的福祉是具有客观性的。第三个论断涉及自然法理论的框架结构……若想更为充分地理解其理论全貌，可以参看他的另一部著作《法理学和政治学中的自然法》。"
            "<br><br>常言道译事艰辛，可世间又有哪一件事是没有代价、苦辛与泪水的呢？幸好在一片汪洋之中，尚有一块块如忒修斯之船般的“浮木”。"
            "<br><br>—— 赵英男，2023 年 12 月 25 日"
        ),
        afterword_note="全文刊于商务印书馆学术中心公众号新书推文。",
        links=[
            ("译后记全文（商务印书馆学术中心公众号）", "http://mp.weixin.qq.com/s?__biz=MzI1NjQyOTIzNA==&mid=2247549783&idx=1&sn=83d95d6f3a74116abfbc8eb5b81bdd52"),
        ],
    ),
    dict(
        title="先例的哲学基础", role="校", year="2026",
        slug="xianli-zhexue-jichu", cover="xianli-zhexue-jichu.jpg",
        tags="先例 · 法哲学",
        meta=[
            ("主编", "[英] 蒂莫西·恩迪科特、[英] 塞巴斯蒂安·刘易斯、[英] 哈夫斯泰因·丹·克里斯蒂安松"),
            ("译者", "高尚 等"),
            ("校者", "赵英男、樊一江"),
            ("出版社", "北京大学出版社"),
            ("出版时间", "2026 年 1 月"),
            ("丛书", "法律今典译丛"),
            ("ISBN", "978-7-301-37206-7"),
            ("页数 / 定价", "全书四十章 / 179.00 元"),
            ("原书", "Philosophical Foundations of Precedent, Oxford University Press, 2023"),
        ],
        intro="本书对先例在法律、司法裁判与道德实践中的作用展开了宏阔、深入且多元的哲学考察。全书共四十章，汇集了当代法哲学界资深领军学者与新锐研究者的广泛成果，对法律及相关实践推理领域中遵循既往裁判的惯习展开了诸多极具创新性的哲学探究；同时，各章亦系统阐释了法院及其他决策主体在偏离既有先例时可能的正当依据。本书为纪念约瑟夫·拉兹而编，赵英男承担其中第二部分（先例与法律论证，第 9–13 章）的翻译并参与全书校订。",
        show_afterword=False,
        afterword_title="关于本书的译后记",
        afterword="本书为多人合译（高尚等译，赵英男、樊一江校），书末译后记由主要译者撰写，不单独收录译者个人后记。如需说明个人承担章节或校订情况，可在此补充。",
        afterword_note="目录显示书末有译后记（主要译者署名）。",
        links=[
            ("出版信息（法律思想公众号）", "http://mp.weixin.qq.com/s?__biz=MzA5MTQ1NDM2Mg==&mid=2656496262&idx=1&sn=12315f3da02eb7b33b3020101b3efae4"),
        ],
    ),
]

# --------------------------------------------------------------- 译后记（外部数据，提取自作者译稿）
# 由各书 raw/trans 或译稿原文抽取，集中存于 content/afterwords.json，便于维护。
_AW_PATH = os.path.join(SITE, "content", "afterwords.json")
if os.path.exists(_AW_PATH):
    with open(_AW_PATH, encoding="utf-8") as _f:
        _AW = json.load(_f)
    for _w in WORKS:
        if _w["slug"] in _AW:
            _a = _AW[_w["slug"]]
            _w["afterword"] = _a["html"]
            _w["afterword_title"] = _a["title"]
            _w["afterword_note"] = _a.get("note", "")

# --------------------------------------------------------------- 排序
# 著作栏目顺序：作者本人「著」置顶；「译」作按出版时间倒序（新出版在前）；
# 「校」排在最后。年份相同按月份倒序，再保稳定序。
def _pub_date(w):
    for k, v in w["meta"]:
        if k == "出版时间":
            m = re.search(r"(\d{4})\s*年\s*(\d{1,2})?", v)
            if m:
                return (int(m.group(1)), int(m.group(2)) if m.group(2) else 1)
    return (0, 0)

_GROUP = {"著": 0, "译": 1, "校": 2}
WORKS.sort(key=lambda w: (_GROUP.get(w["role"], 2), -_pub_date(w)[0], -_pub_date(w)[1]))

# --------------------------------------------------------------- 模板
def header(title, rel=""):
    return f"""<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} · 一般法理学</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{rel}assets/css/style.css?v=2" />
  <link rel="alternate" type="application/rss+xml" title="一般法理学" href="{rel}feed.xml" />
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{rel}index.html">一般法理学</a>
      <button class="menu-toggle" data-menu-toggle aria-label="菜单">菜单</button>
      <nav id="nav-links" class="nav-links">
        <a href="{rel}works.html">著作</a>
        <a href="{rel}reviews.html">书评</a>
        <a href="{rel}teaching.html">教学</a>
        <a href="{rel}updates.html">动态</a>
        <a href="{rel}notes.html">札记</a>
        <a href="{rel}tags.html">标签</a>
        <a href="{rel}about.html">关于</a>
        <button class="icon-btn" data-search-open>搜索</button>
        <button class="icon-btn" data-theme-toggle>主题</button>
      </nav>
    </div>
  </header>
"""

FOOTER = """
  <footer class="site-footer">
    <div class="wrap">
      <span>一般法理学</span>
      <span><a href="{rel}about.html">关于</a> · <a href="{rel}tags.html">标签</a> · <a href="{rel}feed.xml">RSS</a></span>
    </div>
  </footer>

  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <input id="search-input" type="text" placeholder="搜索本站内容…" autocomplete="off" />
      <div class="hint"><span>按 Esc 关闭</span><span>Cmd/Ctrl + K</span></div>
      <button class="icon-btn" data-search-close style="margin-top:.8rem">关闭</button>
    </div>
  </div>

  <script src="{rel}assets/js/site-config.js?v=2"></script>
  <script src="{rel}assets/js/giscus.js?v=2"></script>
  <script src="{rel}assets/js/main.js?v=2"></script>
</body>
</html>
"""

SEARCH_OVERLAY = """
  <div class="search-overlay" id="search-overlay">
    <div class="search-box">
      <input id="search-input" type="text" placeholder="搜索本站内容…" autocomplete="off" />
      <div class="hint"><span>按 Esc 关闭</span><span>Cmd/Ctrl + K</span></div>
      <button class="icon-btn" data-search-close style="margin-top:.8rem">关闭</button>
    </div>
  </div>
"""

def build_grid():
    cards = []
    for w in WORKS:
        slug, cover = w["slug"], w["cover"]
        cards.append(f"""        <article class="work-card" data-searchable data-tags="{w['tags']}">
          <a class="work-cover" href="works/{slug}.html"><img src="assets/covers/{cover}" alt="《{w['title']}》封面" loading="lazy" /></a>
          <div class="work-body">
            <div class="role">{w['role']}</div>
            <h3><a href="works/{slug}.html">{w['title']}</a></h3>
            <div class="year">{w['year']}</div>
          </div>
        </article>""")
    body = f"""{header("著作")}
  <main>
    <section class="wrap-wide">
      <h1 class="page-title">著作</h1>

      <div class="works-grid">
{chr(10).join(cards)}
      </div>
    </section>

    <section class="wrap comments">
      <h2>评论</h2>
      <div id="giscus-mount"></div>
    </section>
  </main>
"""
    with open(os.path.join(SITE, "works.html"), "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel=""))
    print("built works.html (%d works)" % len(WORKS))

def build_detail(w):
    meta_rows = "".join(
        f'<div><span class="meta-k">{k}</span><span class="meta-v">{v}</span></div>'
        for k, v in w["meta"]
    )
    links_html = ""
    if w["links"]:
        items = "".join(f'<li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>' for label, url in w["links"])
        links_html = f'<div class="work-links"><span class="meta-k">相关链接</span><ul>{items}</ul></div>'
    note_html = f'<p class="muted small">{w["afterword_note"]}</p>' if w.get("afterword_note") else ""
    if w.get("show_afterword", True):
        aw_section = (
            f'      <h2>{w["afterword_title"]}</h2>\n'
            f'      <div class="afterword" id="aw-{w["slug"]}">{w["afterword"]}</div>\n'
            f'      <button class="aw-toggle" type="button" data-target="aw-{w["slug"]}" hidden>展开全文</button>\n'
            f"      {note_html}\n"
        )
    else:
        aw_section = ""
    body = f"""{header(w["title"], rel="../")}
  <main>
    <section class="wrap prose">
      <p class="breadcrumb"><a href="../works.html">著作</a> / {w['title']}</p>
      <div class="work-detail">
        <div class="work-cover-lg"><img src="../assets/covers/{w['cover']}" alt="《{w['title']}》封面" /></div>
        <div class="work-detail-body">
          <div class="role-lg">{w['role']}</div>
          <h1 class="page-title">{w['title']}</h1>
          <div class="work-meta">
            {meta_rows}
          </div>
        </div>
      </div>

      <h2>内容简介</h2>
      <p>{w['intro']}</p>

      {aw_section}
      {links_html}

      <div class="comments">
        <h2>评论</h2>
        <div id="giscus-mount"></div>
      </div>
    </section>
  </main>
"""
    path = os.path.join(SITE, "works", w["slug"] + ".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body + FOOTER.format(rel="../"))
    print("built works/%s.html" % w["slug"])

OLD = ["shenjing-quanli-daolun", "fa-de-gainian", "falixue-duben", "bijiaofa-suibi"]

def main():
    os.makedirs(os.path.join(SITE, "works"), exist_ok=True)
    for slug in OLD:
        p = os.path.join(SITE, "works", slug + ".html")
        if os.path.exists(p):
            os.remove(p)
            print("removed old placeholder works/%s.html" % slug)
    build_grid()
    for w in WORKS:
        build_detail(w)

if __name__ == "__main__":
    main()
