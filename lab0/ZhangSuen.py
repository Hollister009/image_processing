class ZhangSuen:
    def __init__(self, image):
        self.image = image
        self.skeleton = self.skeletonize()

    def skeletonize(self):
        image = self.image
        changing1 = changing2 = [(-1, -1)]
        while changing1 or changing2:
            # Step 1
            changing1 = []
            for y in range(1, len(image) - 1):
                for x in range(1, len(image[0]) - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = ZhangSuen.neighbours(x, y, image)
                    if (image[y][x] == 1 and  # (Condition 0)
                            P4 * P6 * P8 == 0 and  # Condition 4
                            P2 * P4 * P6 == 0 and  # Condition 3
                            ZhangSuen.transitions(n) == 1 and  # Condition 2
                            2 <= sum(n) <= 6):  # Condition 1
                        changing1.append((x, y))
            for x, y in changing1: image[y][x] = 0
            # Step 2
            changing2 = []
            for y in range(1, len(image) - 1):
                for x in range(1, len(image[0]) - 1):
                    P2, P3, P4, P5, P6, P7, P8, P9 = n = ZhangSuen.neighbours(x, y, image)
                    if (image[y][x] == 1 and  # (Condition 0)
                            P2 * P6 * P8 == 0 and  # Condition 4
                            P2 * P4 * P8 == 0 and  # Condition 3
                            ZhangSuen.transitions(n) == 1 and  # Condition 2
                            2 <= sum(n) <= 6):  # Condition 1
                        changing2.append((x, y))
            for x, y in changing2: image[y][x] = 0
            # print changing1
            # print changing2
        return image

    @staticmethod
    def neighbours(x, y, image):
        # P2, P3, ..., P9
        points = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
        i = image
        # print((x,y))
        return [i[y + py][x + px] for px, py in points]

    @staticmethod
    def transitions(neighbours):
        n = neighbours + neighbours[0:1]  # P2, ... P9, P2
        return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))
