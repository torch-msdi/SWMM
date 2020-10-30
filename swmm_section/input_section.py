import re


class InpSection(object):
    """
    从inp文件中提取矩形、非规则、圆形断面的几何信息
    请调用其中的section_data方法来提取断面数据
    2020.10.26日，该版本目前只支持非规则断面、圆管及矩形断面的提取
    """

    def __init__(self, path):
        """
        读取inp文件
        :param path: 文件路径 e.g:...\1.inp
        """
        with open(path, 'r') as f:
            f = f.readlines()
        index, counter = [], []
        number = 0
        self.current_number = 0
        self.file = f
        self.index_marker = []
        self.sections = self.section_data
        for i in self.sections:
            index.append(number)
            counter.append(i)
        self.index_name = dict(zip(index, counter))
        self.name_index = dict(zip(counter, index))

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_number < len(self.sections):
            ret = self.index_name[self.current_number]
            data = self.sections[self.index_name[self.current_number]]
            result = {ret: data}
            self.current_number += 1
            return result
        else:
            raise StopIteration

    def get_marker(self):
        """
        工具函数，获取与断面相关选项卡的行号，记录在index_marker中
        :return:
        """
        for lines_index in range(len(self.file)):
            # 提取管线-断面对应数据
            if self.file[lines_index] == '[CONDUITS]\n':
                self.index_marker.append(lines_index + 3)
            # 提取断面数据
            if self.file[lines_index] == '[XSECTIONS]\n':
                self.index_marker.append(lines_index + 3)
            # 提取不规则断面对应数据
            if self.file[lines_index] == '[TRANSECTS]\n':
                self.index_marker.append(lines_index + 4)
                break
        return self.index_marker, self.file

    @staticmethod
    def export_data(data, start_line):
        """
        截取选项卡内的数据
        :param start_line: input文件中[XSECTION]的起始行号
        :param data: input文件列表格式
        :return: 选项卡内的有效数据
        """
        result = 0  # 终止行号
        temp_data = data[start_line: -1]
        for index in range(len(temp_data)):
            try:
                if temp_data[index][0] == '[':
                    result = index
                    break
            except IndexError:
                pass
        return temp_data[: result - 1]

    @property
    def section_data(self):
        """
        返回断面数据
        :return:
        {"circle": {'DM1': 1, 'DM2': 3},
        "irregular": {'DM3': [[0, 1, 2], [3,2,3]]},
        "rectangle": {'DM4': {'height': 2, 'width': 3}}
        }
        """
        index_marker, f = self.get_marker()
        # 标记conduits\section\irregular选项卡的位置
        conduits = self.export_data(data=f, start_line=index_marker[0])
        section = self.export_data(data=f, start_line=index_marker[1])
        irregular = self.export_data(data=f, start_line=index_marker[2])
        irregular.append(';\n')
        conduits_name = []

        # 获取所有断面名称
        for conduit in conduits:
            conduits_name.append(re.split(r' +', conduit)[0])
        result = {}
        for conduit_index in range(len(conduits_name)):
            shape = re.split(r' +', section[conduit_index])[1]
            conduit_name = re.split(r' +', section[conduit_index])[0]
            # 提取矩形断面
            if shape == 'RECT_OPEN':
                right = float(re.split(r' +', section[conduit_index])[3])
                top = float(re.split(r' +', section[conduit_index])[2])
                # noinspection PyTypeChecker
                result[conduit_name] = {'data': {
                    'height': top, 'width': right}, 'type': 'rectangle'}

            # 提取非规则断面
            elif shape == 'IRREGULAR':
                start_pointer = 0
                for i in range(len(irregular)):
                    if irregular[i] == ';\n':
                        x_list, z_list = [], []
                        end_pointer = i + 1
                        data = irregular[start_pointer: end_pointer]
                        conduit_name = re.split(r' +', data[0])[1]
                        start_pointer = end_pointer + 1
                        temp_data = data[1: -1]
                        for line in temp_data:
                            x_z = re.split(r' +', line)
                            del x_z[0]
                            for index in range(int(len(x_z) / 2)):
                                x_list.append(float(x_z[index * 2 + 1]))
                                z_list.append(float(x_z[index * 2]))
                        result[conduit_name] = {'data': [x_list, z_list], 'type': 'irregular'}

            # 提取圆管
            elif shape == 'CIRCULAR':
                diameter = float(re.split(r' +', section[conduit_index])[2])
                result[conduit_name] = {'data': diameter, 'type': 'circle'}

        return result

    def __len__(self):
        return len(self.sections)
