import unittest
import os

from question_classifier import QuestionClassifier
from question_parser import QuestionParser
from answer_search import AnswerSearcher

os.chdir(os.path.join(os.getcwd(), '..'))


class AnswerTest(unittest.TestCase):

    qc = QuestionClassifier()
    qp = QuestionParser()
    ss = AnswerSearcher()

    def search(self, question: str):
        res = self.qc.classify(question)
        if res is None or res.is_qt_null():
            return None
        res = self.qp.parse(res)
        ans = self.ss.search(res)
        return ans

    def test_year_status(self):
        self.assertEqual(self.search('2011年总体情况怎样？'),
                         '2011年，全年航空安全形势稳定，旅客运输和通用航空保持较快增长，运行质量和经济效益得到提升，基础设施建设取得新成绩，结构调整和深化改革迈出新步伐，党的建设和行业文化建设得到加强。')
        self.assertEqual(self.search('2011年发展形势怎样？'),
                         '2011年，全年航空安全形势稳定，旅客运输和通用航空保持较快增长，运行质量和经济效益得到提升，基础设施建设取得新成绩，结构调整和深化改革迈出新步伐，党的建设和行业文化建设得到加强。')
        self.assertEqual(self.search('2011年发展如何？'),
                         '2011年，全年航空安全形势稳定，旅客运输和通用航空保持较快增长，运行质量和经济效益得到提升，基础设施建设取得新成绩，结构调整和深化改革迈出新步伐，党的建设和行业文化建设得到加强。')
        self.assertEqual(self.search('15年形势怎样？'),
                         None)

    def test_catalog_status(self):
        self.assertEqual(self.search('2011年运输航空总体情况怎样？'),
                         '运输航空在2011年，民航运输发展稳中向好，实现了“十二五”时期的良好开局。')
        self.assertEqual(self.search('2011年航空安全发展形势怎样？'),
                         '航空安全在2011年，民航绝大多数运行单位安全形势平稳。全行业没有发生空防安全事故、重大航空地面事故和特大航空器维修事故。')
        self.assertEqual(self.search('2011年教育及科技发展如何？'),
                         '并没有关于2011年教育及科技的描述。')
        self.assertEqual(self.search('2011固定资产投资形势怎样？'),
                         '并没有关于2011年固定资产投资的描述。')
        self.assertEqual(self.search('2011固定资产投资和航空安全发展形势怎样？'),
                         '并没有关于2011年固定资产投资的描述；航空安全在2011年，民航绝大多数运行单位安全形势平稳。全行业没有发生空防安全事故、重大航空地面事故和特大航空器维修事故。')

    def test_exist_catalog(self):
        self.assertEqual(self.search('2011年有哪些指标目录？'),
                         '2011年目录包括: 社会责任，固定资产投资，通用航空，经济效益，运输航空，教育及科技，航空安全，航空服务，运输效率与收入。')
        self.assertEqual(self.search('2011年有哪些基准？'),
                         '2011年目录包括: 社会责任，固定资产投资，通用航空，经济效益，运输航空，教育及科技，航空安全，航空服务，运输效率与收入。')
        self.assertEqual(self.search('2011年有啥规格？'),
                         '2011年目录包括: 社会责任，固定资产投资，通用航空，经济效益，运输航空，教育及科技，航空安全，航空服务，运输效率与收入。')
        self.assertEqual(self.search('2012年的目录有哪些？'),
                         '2012年目录包括: 教育及科技，运输航空，飞行员数量，经济效益，通用航空，固定资产投资，社会责任，运输效率与收入，航空服务，航空安全。')

    def test_index_value(self):
        self.assertEqual(self.search('2011年的货邮周转量和游客周转量是多少？'),
                         '货邮周转量为173.91亿吨公里；旅客周转量为403.53亿吨公里。')
        self.assertEqual(self.search('2011年的货邮周转量的值是？'),
                         '货邮周转量为173.91亿吨公里。')
        self.assertEqual(self.search('2011年的货邮周转量为？'),
                         '货邮周转量为173.91亿吨公里。')
        self.assertEqual(self.search('2011年的货邮周转量是'),
                         '货邮周转量为173.91亿吨公里。')

    def test_area_value(self):
        self.assertEqual(self.search('11年国内的运输总周转量为？'),
                         '国内航线运输总周转量为380.61亿吨公里。')
        self.assertEqual(self.search('11年国内的运总周转量为？'),
                         '国内航线运输总周转量为380.61亿吨公里。')
        self.assertEqual(self.search('11年国内和国际的旅客运输量为'),
                         '国内航线旅客运输量为27199.0万人次；国际航线旅客运输量为2118.0万人次。')
        self.assertEqual(self.search('11年国内和国际的游客运输量为'),
                         '国内航线旅客运输量为27199.0万人次；国际航线旅客运输量为2118.0万人次。')
        self.assertEqual(self.search('11年国际方面运输总周转量是多少？'),
                         '国际航线运输总周转量为196.84亿吨公里。')
        self.assertEqual(self.search('11年国际方面运输总周转量和货邮周转量是多少？'),
                         '国际航线运输总周转量为196.84亿吨公里；国际货邮周转量，无数据记录。')
        self.assertEqual(self.search('11年国内和国际方面运输总周转量和货邮周转量是多少？'),
                         '国内航线运输总周转量为380.61亿吨公里；国内货邮周转量，无数据记录；国际航线运输总周转量为196.84亿吨公里；国际货邮周转量，无数据记录。')

    def test_index_overall(self):
        self.assertEqual(self.search('2011年的游客周转量和运输总周转量占总体多少？'),
                         '无运输总周转量的父级数据记录，无法比较；旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011年的游客周转量占父指标多少份额？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011年的游客周转量是总体的多少倍？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011游客周转量占总体的百分之多少？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011年的游客周转量为其总体的多少倍？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011游客周转量占总量的多少？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')
        self.assertEqual(self.search('2011年游客周转量占有总额的多少比例？'),
                         '旅客周转量为403.53亿吨公里，其占总体（运输总周转量）的69.88%，总体（运输总周转量）是其的1.431倍。')

    def test_index_2_overall(self):
        self.assertEqual(self.search('2012年游客周转量占总体的百分比比去年变化多少？'),
                         '2012年旅客周转量为446.43亿吨公里，其总体指标（运输总周转量）的为610.32亿吨公里，约占总体的73.15%；2011年旅客周转量为403.53亿吨公里，其总体指标（运输总周转量）的为577.44亿吨公里，约占总体的69.88%；前者相比后者提高3.27%。')
        self.assertEqual(self.search('2012年游客周转量占总体的百分比，相比11年变化多少？'),
                         '2012年旅客周转量为446.43亿吨公里，其总体指标（运输总周转量）的为610.32亿吨公里，约占总体的73.15%；2011年旅客周转量为403.53亿吨公里，其总体指标（运输总周转量）的为577.44亿吨公里，约占总体的69.88%；前者相比后者提高3.27%。')
        self.assertEqual(self.search('2012年相比11年，游客周转量占总体的百分比变化多少？'),
                         '2012年旅客周转量为446.43亿吨公里，其总体指标（运输总周转量）的为610.32亿吨公里，约占总体的73.15%；2011年旅客周转量为403.53亿吨公里，其总体指标（运输总周转量）的为577.44亿吨公里，约占总体的69.88%；前者相比后者提高3.27%。')
        self.assertEqual(self.search('2012年的游客周转量占总计比例比去年增加多少？'),
                         '2012年旅客周转量为446.43亿吨公里，其总体指标（运输总周转量）的为610.32亿吨公里，约占总体的73.15%；2011年旅客周转量为403.53亿吨公里，其总体指标（运输总周转量）的为577.44亿吨公里，约占总体的69.88%；前者相比后者提高3.27%。')
        self.assertEqual(self.search('2012年的运输总周转量占父级的倍数比11年降低多少？'),
                         '无2012、2011这几年运输总周转量的父级数据记录，无法比较。')

    def test_indexes_m_compare(self):
        self.assertEqual(self.search('2011年游客周转量是货邮周转量的几倍？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者是后者的0.431倍，后者是前者的2.32倍。')
        self.assertEqual(self.search('11年游客周转量是旅客运输量的几倍？'),
                         '旅客运输量的单位（万人次）与旅客周转量的单位（亿吨公里）不同，无法比较。')
        self.assertEqual(self.search('11年游客周转量是新增机场的几倍？'),
                         '新增机场的单位（None）与旅客周转量的单位（亿吨公里）不同，无法比较。')
        self.assertEqual(self.search('2011年游客周转量是货邮周转量的百分之几？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者是后者的0.431倍，后者是前者的2.32倍。')

    def test_indexes_2m_compare(self):
        self.assertEqual(self.search('2011年游客周转量是12年的百分之几？'),
                         '2011年的旅客周转量（403.53亿吨公里）是2012年的（446.43亿吨公里）0.904倍。')
        self.assertEqual(self.search('2011年的是12年货邮周转量的百分之几？'),
                         '2011年的货邮周转量（173.91亿吨公里）是2012年的（163.89亿吨公里）1.061倍。')
        self.assertEqual(self.search('2011年旅客运输量占12的百分之？'),
                         '2011年的旅客运输量（29317.0万人次）是2012年的（31936.0万人次）0.918倍。')
        self.assertEqual(self.search('2011年游客周转量是13年的几倍？'),
                         '2011年的旅客周转量（403.53亿吨公里）是2013年的（501.43亿吨公里）0.805倍。')
        self.assertEqual(self.search('2011年游客周转量为12年的多少倍？'),
                         '2011年的旅客周转量（403.53亿吨公里）是2012年的（446.43亿吨公里）0.904倍。')
        self.assertEqual(self.search('2011年游客周转量和运输总周转量为12年的多少倍？'),
                         '2011年的运输总周转量（577.44亿吨公里）是2012年的（610.32亿吨公里）0.946倍。')

    def test_indexes_n_compare(self):
        self.assertEqual(self.search('11年游客周转量比货邮周转量多多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比游客运输量大？'),
                         '旅客周转量的单位（亿吨公里）与旅客运输量的单位（万人次）不同，无法比较。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量少多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量增加了多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量降低了？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量降低了？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量变化了多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量比货邮周转量变了？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量与货邮周转量相比降低了多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量与货邮周转量比，降低了多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')
        self.assertEqual(self.search('11年游客周转量与货邮周转量比较 降低了多少？'),
                         '货邮周转量为173.91亿吨公里，旅客周转量为403.53亿吨公里，前者比后者少229.62亿吨公里。')

    def test_indexes_2n_compare(self):
        self.assertEqual(self.search('2011年游客周转量比12年降低了？'),
                         '2011年的旅客周转量（403.53亿吨公里）比2012年的（446.43亿吨公里）减少42.9亿吨公里。')
        self.assertEqual(self.search('2012年游客周转量比去年增加了？'),
                         '2012年的旅客周转量（446.43亿吨公里）比2011年的（403.53亿吨公里）增加42.9亿吨公里。')
        self.assertEqual(self.search('2012年节能减排比去年多了多少？'),
                         '节能减排的记录为无效的值类型，无法比较。')
        self.assertEqual(self.search('12年的货邮周转量比去年变化了多少？'),
                         '2012年的货邮周转量（163.89亿吨公里）比2011年的（173.91亿吨公里）减少10.02亿吨公里。')
        self.assertEqual(self.search('12年的货邮周转量同去年相比变化了多少？'),
                         '2012年的货邮周转量（163.89亿吨公里）比2011年的（173.91亿吨公里）减少10.02亿吨公里。')
        self.assertEqual(self.search('13年的货邮周转量同2年前相比变化了多少？'),
                         '2013年的货邮周转量（170.29亿吨公里）比2011年的（173.91亿吨公里）减少3.62亿吨公里。')
        self.assertEqual(self.search('12年同去年相比，货邮周转量变化了多少？'),
                         '2012年的货邮周转量（163.89亿吨公里）比2011年的（173.91亿吨公里）减少10.02亿吨公里。')

    def test_indexes_g_compare(self):
        self.assertEqual(self.search('2012年游客周转量同比增长多少？'),
                         '2012年的旅客周转量为446.43亿吨公里，其去年的为403.53亿吨公里，同比增长10.63%。')
        self.assertEqual(self.search('2012年重大运输任务同比增长多少？'),
                         '2012年重大运输任务的记录非数值类型，无法计算；2012年重大运输任务的记录非数值类型，无法计算。')
        self.assertEqual(self.search('2012年游客周转量同比下降百分之几？'),
                         '2012年的旅客周转量为446.43亿吨公里，其去年的为403.53亿吨公里，同比增长10.63%。')
        self.assertEqual(self.search('2012年游客周转量和货邮周转量同比下降百分之几？'),
                         '2012年的货邮周转量为163.89亿吨公里，其去年的为173.91亿吨公里，同比降低5.76%；2012年的旅客周转量为446.43亿吨公里，其去年的为403.53亿吨公里，同比增长10.63%。')

    def test_area_overall(self):
        self.assertEqual(self.search('11年国内的货邮周转量占总体的百分之几？'),
                         '国内无货邮周转量的数据记录，无法比较。')
        self.assertEqual(self.search('11年国内的旅客运输量占总体的百分之几？'),
                         '国内无旅客运输量父级地区的数据记录，无法比较。')
        self.assertEqual(self.search('11年国际和国内的运输总周转量占总值的多少？'),
                         '国际无运输总周转量父级地区的数据记录，无法比较；国内无运输总周转量父级地区的数据记录，无法比较。')
        self.assertEqual(self.search('11年国有控股的运输航空公司占全部的多少？'),
                         '国有控股无运输航空公司父级地区的数据记录，无法比较。')
        self.assertEqual(self.search('11年我国西部地区的运输总周转量和货邮吞吐量是全体的多少倍？'),
                         '西部地区无运输总周转量的数据记录，无法比较。')
        self.assertEqual(self.search('11年港澳台和国际的运输总周转量和旅客运输量是父级的多少倍？'),
                         '港澳台航线的运输总周转量为12.64亿吨公里，其占国内运输总周转量的3.32%，国内运输总周转量是其的30.112倍；港澳台无旅客运输量父级地区的数据记录，无法比较。')

    def test_area_2_overall(self):
        self.assertEqual(self.search('2012年港澳台的游客运输量占总体的百分比比去年变化多少？'),
                         '2012年港澳台旅客运输量为834.0万人次，其总体地区（国内）的为29600.0万人次，约占总体的2.82%；2011年港澳台旅客运输量为760.0万人次，其总体地区（国内）的为27199.0万人次，约占总体的2.79%；前者相比后者提高0.03%。')
        self.assertEqual(self.search('2012年中部地区旅客吞吐量占总体的百分比，相比11年变化多少？'),
                         '无2012、2011这几年中部地区旅客吞吐量的父级数据记录，无法比较。')
        self.assertEqual(self.search('2012年相比11年，港澳台游客运输量占总体的百分比变化多少？'),
                         '2012年港澳台旅客运输量为834.0万人次，其总体地区（国内）的为29600.0万人次，约占总体的2.82%；2011年港澳台旅客运输量为760.0万人次，其总体地区（国内）的为27199.0万人次，约占总体的2.79%；前者相比后者提高0.03%。')
        self.assertEqual(self.search('2012年的国内游客周转量占总计比例比去年增加多少？'),
                         '无2012、2011这几年国内旅客周转量的数据记录，无法比较。')
        self.assertEqual(self.search('2012年的国际运输总周转量占父级的倍数比11年降低多少？'),
                         '无2012、2011这几年国际运输总周转量的父级数据记录，无法比较。')

    def test_areas_m_compare(self):
        self.assertEqual(self.search('11年港澳台货邮周转量占国内的百分之几？'),
                         '无港澳台货邮周转量数据记录，无法比较。')
        self.assertEqual(self.search('11年国内的运输总周转量是港澳台的几倍？'),
                         '国内航线的运输总周转量为380.61亿吨公里，港澳台航线的运输总周转量为12.64亿吨公里，前者是后者的30.112倍，后者是前者的0.033倍。')
        self.assertEqual(self.search('11年国际运输总周转量是国内的多少倍？'),
                         '国际航线的运输总周转量为196.84亿吨公里，国内航线的运输总周转量为380.61亿吨公里，前者是后者的0.517倍，后者是前者的1.934倍。')
        self.assertEqual(self.search('11年港澳台运输总周转量和游客周转量是国际的多少倍？'),
                         '港澳台航线的运输总周转量为12.64亿吨公里，国际航线的运输总周转量为196.84亿吨公里，前者是后者的0.064倍，后者是前者的15.573倍；无港澳台旅客周转量数据记录，无法比较。')

    def test_areas_2m_compare(self):
        self.assertEqual(self.search('11年港澳台运输总周转量和旅客吞吐量是12年的多少倍？'),
                         '2011年的港澳台运输总周转量（12.64亿吨公里）是2012年的（13.66亿吨公里）0.925倍。')
        self.assertEqual(self.search('12年的是11年港澳台运输总周转量的多少倍？'),
                         '2012年的港澳台运输总周转量（13.66亿吨公里）是2011年的（12.64亿吨公里）1.081倍。')
        self.assertEqual(self.search('12年国内与国际货邮周转量占11年百分之几？'),
                         '无关于2012年的国内货邮周转量的记录；无关于2012年的国际货邮周转量的记录。')
        self.assertEqual(self.search('12年国际运输总周转量是11年比例？'),
                         '2012年的国际运输总周转量（194.49亿吨公里）是2011年的（196.84亿吨公里）0.988倍。')

    def test_areas_n_compare(self):
        self.assertEqual(self.search('2011年国内货邮运输量比国际多多少？'),
                         '国内航线的货邮运输量为379.4万吨，国际航线的货邮运输量为178.1万吨，前者比后者多201.3万吨。')
        self.assertEqual(self.search('2011年港澳台游客运输量比国内的少多少？'),
                         '港澳台航线的旅客运输量为760.0万人次，国内航线的旅客运输量为27199.0万人次，前者比后者少26439.0万人次。')
        self.assertEqual(self.search('2011年港澳台游客运输量与国内的相比降低多少？'),
                         '港澳台航线的旅客运输量为760.0万人次，国内航线的旅客运输量为27199.0万人次，前者比后者少26439.0万人次。')
        self.assertEqual(self.search('2011年港澳台与国内的相比游客周转量降低多少？'),
                         '无港澳台旅客周转量数据记录，无法比较。')
        self.assertEqual(self.search('11年港澳台货邮周转量和游客周转量比国际的多多少？'),
                         '无港澳台货邮周转量数据记录，无法比较；无港澳台旅客周转量数据记录，无法比较。')

    def test_areas_2n_compare(self):
        self.assertEqual(self.search('2011年国内运输总周转量比一二年多多少？'),
                         '2011年的国内运输总周转量（380.61亿吨公里）比2012年的（415.83亿吨公里）减少35.22亿吨公里。')
        self.assertEqual(self.search('2012年港澳台的游客运输量比上一年的少多少？'),
                         '2012年的港澳台旅客运输量（834.0万人次）比2011年的（760.0万人次）增加74.0万人次。')
        self.assertEqual(self.search('2011年港澳台与国内的游客周转量相比12降低多少？'),
                         '无关于2011年的港澳台旅客周转量的记录；无关于2011年的国内旅客周转量的记录。')
        self.assertEqual(self.search('2011年港澳台的旅客运输量同2012相比降低多少？'),
                         '2011年的港澳台旅客运输量（760.0万人次）比2012年的（834.0万人次）减少74.0万人次。')
        self.assertEqual(self.search('2012年的东部地区与去年相比，货邮吞吐量降低多少？'),
                         '2012年的东部地区货邮吞吐量（926.37万吨）比2011年的（905.98万吨）增加20.39万吨。')
        self.assertEqual(self.search('2012年的北上广与一年前相比，旅客吞吐量降低多少？'),
                         '无关于2012年的北上广旅客吞吐量的记录。')

    def test_areas_g_compare(self):
        self.assertEqual(self.search('2012年国内运输总周转量同比增长了？'),
                         '2012年的国内运输总周转量为415.83亿吨公里，其去年的为380.61亿吨公里，同比增长9.25%。')
        self.assertEqual(self.search('2012年中部地区旅客吞吐量同比下降了多少？'),
                         '2012年的中部地区旅客吞吐量为0.67亿人次，其去年的为0.59亿人次，同比增长13.56%。')
        self.assertEqual(self.search('2012年国内游客周转量和货邮运输量同比变化了多少？'),
                         '2012年的国内货邮运输量为388.5万吨，其去年的为379.4万吨，同比增长2.4%；无2012年关于国内旅客周转量的数据。')

    def test_index_compose(self):
        self.assertEqual(self.search('2011年运输总周转量的子集有？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011年运输总周转量的子集有？.html。')
        self.assertEqual(self.search('2011年航空公司计划航班的组成？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011年航空公司计划航班的组成？.html。')
        self.assertEqual(self.search('2011年指标停用机场的组成有哪些？'),
                         '指标“停用机场”没有任何组成。')
        self.assertEqual(self.search('2011年全行业累计实现营业收入的子指标组成情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011年全行业累计实现营业收入的子指标组成情况？.html。')
        self.assertEqual(self.search('2011年运输总周转量和货邮周转量的子指标组成情况？'),
                         '指标“货邮周转量”没有任何组成。')

    def test_catalog_change(self):
        self.assertEqual(self.search('12年比11年多了哪些目录'),
                         '2011年与2012年相比，未统计1个目录：飞行员数量；2012年与2011年的目录相同。')
        self.assertEqual(self.search('12年比去年增加了哪些目录'),
                         '2011年与2012年相比，未统计1个目录：飞行员数量；2012年与2011年的目录相同。')
        self.assertEqual(self.search('12年比去年少了哪些标准？'),
                         '2011年与2012年相比，未统计1个目录：飞行员数量；2012年与2011年的目录相同。')
        self.assertEqual(self.search('12年与去年相比，目录变化如何？'),
                         '2011年与2012年相比，未统计1个目录：飞行员数量；2012年与2011年的目录相同。')

    def test_index_change(self):
        # 回答中的词语出现位置不固定
        pass

    def test_indexes_change(self):
        self.assertEqual(self.search('2011-13年指标变化情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年指标变化情况？.html。')
        self.assertEqual(self.search('2011-13年指标变化趋势情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年指标变化趋势情况？.html。')

    def test_catalogs_change(self):
        self.assertEqual(self.search('2011-13年目录变化情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年目录变化情况？.html。')
        self.assertEqual(self.search('2011-13年规范趋势情况变化？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年规范趋势情况变化？.html。')

    def test_indexes_trend(self):
        self.assertEqual(self.search('2011-13年运输总周转量的变化趋势如何？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年运输总周转量的变化趋势如何？.html。')
        self.assertEqual(self.search('2011-13年节能减排情况？'),
                         '指标“节能减排”非数值类型，无法比较。')
        self.assertEqual(self.search('2011-13年运输总周转量和旅客周转量情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年运输总周转量和旅客周转量情况？.html。')
        self.assertEqual(self.search('2011-14年运输总周转量值分布状况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-14年运输总周转量值分布状况？.html。')
        self.assertEqual(self.search('2013年运输总周转量值与前两年相比变化状况如何？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2013年运输总周转量值与前两年相比变化状况如何？.html。')

    def test_areas_trend(self):
        self.assertEqual(self.search('2011-13年国内运输总周转量的变化趋势如何？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年国内运输总周转量的变化趋势如何？.html。')
        self.assertEqual(self.search('2011-13年国际运输总周转量情况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年国际运输总周转量情况？.html。')
        self.assertEqual(self.search('2011-13年港澳台运输总周转量值分布状况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年港澳台运输总周转量值分布状况？.html。')

    def test_indexes_overall_trend(self):
        self.assertEqual(self.search('2011-13年货邮周转量占总体的比例的变化形势？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年货邮周转量占总体的比例的变化形势？.html。')
        self.assertEqual(self.search('2011-13年货邮周转量和货邮吞吐量占总体的比例的变化形势？'),
                         '无关于”货邮吞吐量“的父级记录；该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年货邮周转量和货邮吞吐量占总体的比例的变化形势？.html。')
        self.assertEqual(self.search('2011-13年货邮周转量和小型飞机平均日利用率占总体的比例的变化形势？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年货邮周转量和小型飞机平均日利用率占总体的比例的变化形势？.html。')
        self.assertEqual(self.search('2011-13年停用机场占父级指标比的情况？'),
                         '无关于”停用机场“的父级记录。')
        self.assertEqual(self.search('2011-13年民航直属院校在校研究生占总比的分布状况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年民航直属院校在校研究生占总比的分布状况？.html。')
        self.assertEqual(self.search('2011-13年民航直属院校在校研究生和民航直属院校在校中专生占总比的分布状况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年民航直属院校在校研究生和民航直属院校在校中专生占总比的分布状况？.html。')

    def test_areas_overall_trend(self):
        self.assertEqual(self.search('2011-13年国内运输总周转量占总体的比例的变化形势？'),
                         '无关于”国内运输总周转量“的父级记录。')
        self.assertEqual(self.search('2011-13年国际货邮周转量和旅客周转量占父级指标比的情况？'),
                         '无关于”国际货邮周转量“的记录。')
        self.assertEqual(self.search('2011-13年港澳台运输总周转量值占总比的分布状况？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年港澳台运输总周转量值占总比的分布状况？.html。')

    def test_indexes_and_areas_max(self):
        self.assertEqual(self.search('2011-13年运输总周转量最大值是？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年运输总周转量最大值是？.html。')
        self.assertEqual(self.search('2011-13年运输总周转量最小值是哪一年？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年运输总周转量最小值是哪一年？.html。')
        self.assertEqual(self.search('2011-13年国内运输总周转量最大值是？'),
                         '该问题的回答已渲染为图像，详见：results/qa-cakg-2011-13年国内运输总周转量最大值是？.html。')

    def test_begin_stats(self):
        self.assertEqual(self.search('哪年统计了航空严重事故征候？'),
                         '指标“严重事故征候”最早于2011年开始统计；指标“事故征候”最早于2011年开始统计。')
        self.assertEqual(self.search('在哪一年出现了航空公司营业收入数据？'),
                         '指标“航空公司实现营业收入”最早于2011年开始统计。')
        self.assertEqual(self.search('航空事故征候数据统计出现在哪一年？'),
                         '指标“事故征候”最早于2011年开始统计。')
        self.assertEqual(self.search('运输周转量数据统计出现在哪一年？'),
                         '指标“运输总周转量”最早于2011年开始统计。')


if __name__ == '__main__':
    unittest.main()