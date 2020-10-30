from input_section import InpSection
import pandas as pd
from deal_data import deal


sections = InpSection(path='data/XiaoXiHe.inp')  # 实例化断面形态
raw_dict = pd.read_excel('data/XiaoXiHe-link.xlsx', None)  # 获取原始数据
for key in raw_dict:
    raw_dict[key] = raw_dict[key].to_dict('list')


if __name__ == '__main__':
    # 计算现状下断面形态参数
    raw_result, raw_log = deal(sections=sections, excel_data=raw_dict['Sheet1'])

    # 计算设计工况下断面形态参数
    design_result, design_log = deal(sections=sections, excel_data=raw_dict['Sheet2'])

    # 计算湿周率
    wet_circle = []
    for i in range(len(raw_result['湿周'])):
        try:
            wet_circle.append(raw_result['湿周'][i]/design_result['湿周'][i])
        except ZeroDivisionError:
            wet_circle.append(0)
    raw_result['湿周率'] = wet_circle

    # 输出结果
    result_df = pd.DataFrame(raw_result)
    for i in raw_log:
        print(i)
    result_df.to_excel('result/result.xlsx', index=False)
    print('导出结果成功！')
