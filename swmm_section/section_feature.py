import math


class SectionFeature(object):
    """
    单个断面计算方法
    """

    def __init__(self, data, depth):
        """
        :param data: 断面数据 e.g {'data':1, 'type': 'circle'}
        """
        self.data = data
        self.depth = max(0, depth)

    def section_area(self):
        """
        返回指定水深下的过水断面面积
        :return:
        """
        if self.data['type'] == 'circle':
            """定积分求圆面积"""
            r = self.data['data'] / 2  # r为圆半径
            # 水深大于管径时，调整为管径
            if self.depth > 2 * r:
                self.depth = 2 * r
            width = 2 * (r ** 2 - (r - self.depth) ** 2) ** 0.5  # 勾股定理
            cos_degree = 1 - width ** 2 / (2 * r ** 2)  # 余弦定理
            angle = math.acos(cos_degree)
            if self.depth < r:
                total_area = math.pi * r**2 * angle / (2 * math.pi)
                triangle_area = width * (r - self.depth) / 2
                return total_area - triangle_area
            else:
                total_area = math.pi * r ** 2 * angle / (2 * math.pi)
                triangle_area = width * (r - self.depth) / 2
                return math.pi * r**2 - total_area + triangle_area

        elif self.data['type'] == 'rectangle':
            """矩形断面面积求法"""
            return abs(self.depth) * self.data['data']['width']

        elif self.data['type'] == 'irregular':
            """非规则断面面积求法"""
            area = 0
            x_list, z_list = self.data['data'][0], self.data['data'][1]
            minor_z = min(z_list)
            z_list = [i-minor_z for i in z_list]
            for delta_index in range(len(x_list) - 1):
                x = [x_list[delta_index], x_list[delta_index + 1]]
                z = [z_list[delta_index], z_list[delta_index + 1]]
                delta_area = abs(x[0] - x[1]) * abs(z[0] - z[1]) / 2
                if self.depth >= max(z):
                    area += delta_area + abs(x[0] - x[1])*abs(self.depth-max(z))
                elif self.depth <= min(z):
                    pass
                else:
                    ratio = self.depth / abs(z[0] - z[1])
                    area += ratio**2 * delta_area
            return area

    def avg_water_depth(self):
        """
        计算给定水深下的断面平均水深
        :return:
        """
        area = self.section_area()
        try:
            return area/self.water_width()
        except ZeroDivisionError:
            return 0

    def water_width(self):
        """
        返回指定水深下的水面宽度
        :return:
        """
        if self.data['type'] == 'circle':
            r = self.data['data'] / 2
            if self.depth > r:
                return 2 * r
            else:
                return 2 * (r**2 - (r - self.depth)**2)**0.5

        elif self.data['type'] == 'rectangle':
            return self.data['data']['width']

        elif self.data['type'] == 'irregular':
            width = 0
            x_list, z_list = self.data['data'][0], self.data['data'][1]
            minor_z = min(z_list)
            z_list = [i-minor_z for i in z_list]
            for delta_index in range(len(x_list) - 1):
                x = [x_list[delta_index], x_list[delta_index + 1]]
                z = [z_list[delta_index], z_list[delta_index + 1]]
                delta_with = abs(x[0] - x[1])
                if self.depth >= max(z):
                    width += delta_with
                elif self.depth <= min(z):
                    pass
                else:
                    ratio = self.depth / abs(z[0] - z[1])
                    width += ratio * delta_with
            return width

    def wet_circle(self):
        """
        返回指定水深下的湿周
        :return:
        """
        if self.data['type'] == 'circle':
            r = self.data['data'] / 2
            if self.depth < r:
                width = 2 * (r**2 - (r - self.depth)**2)**0.5  # 勾股定理
                cos_degree = 1 - width**2 / (2 * r**2)  # 余弦定理
                angle = math.acos(cos_degree)
                wet_circle = angle * r
                return wet_circle
            elif self.depth > 2 * r:
                return 2 * math.pi * r
            else:
                width = 2 * (r ** 2 - (r - self.depth) ** 2) ** 0.5  # 勾股定理
                cos_degree = 1 - width ** 2 / (2 * r ** 2)
                angle = 2 * math.pi - math.acos(cos_degree)
                wet_circle = angle * r
                return wet_circle
        elif self.data['type'] == 'rectangle':
            return 2 * self.depth + self.data['data']['width']
        elif self.data['type'] == 'irregular':
            width = 0
            x_list, z_list = self.data['data'][0], self.data['data'][1]
            minor_z = min(z_list)
            z_list = [i-minor_z for i in z_list]
            for delta_index in range(len(x_list) - 1):
                x = [x_list[delta_index], x_list[delta_index + 1]]
                z = [z_list[delta_index], z_list[delta_index + 1]]
                delta_wet = ((x[0] - x[1])**2 + (z[0] - z[1])**2)**0.5
                if self.depth >= max(z):
                    width += delta_wet
                elif self.depth <= min(z):
                    pass
                else:
                    ratio = self.depth / abs(z[0] - z[1])
                    width += ratio * delta_wet
            return width
