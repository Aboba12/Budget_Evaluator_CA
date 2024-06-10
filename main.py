
class three_houses_district:
    prices_r = {1: [6456789, 6678900, 6134567, 6098345, 6347980, 6067890, 6647678, 6093456],
                     2: [6345678, 6098456, 6098456, 6495789, 6145987, 6234869, 6064945, 6048568],
                     3: {True: [6778459, 6933456, 6943056, 6943345, 6924334, 6903234], False: [6067346, 6024567, 6478345, 6568456, 6068324, 6098456, 6067234], None: [6778459, 6933456, 6943056, 6943345, 6924334, 6903234, 6067346, 6024567, 6478345, 6568456, 6068324, 6098456, 6067234]},
                     4: {True: [6934536, 6430433, 6923587, 6823607, 6923687, 6932543], False: [6056723, 6423678, 6023243, 6032856, 6032934, 6065784, 6056324], None: [6934536, 6430433, 6923587, 6823607, 6923687, 6932543, 6056723, 6423678, 6023243, 6032856, 6032934, 6065784, 6056324]},
                     5: {True: [6323034, 6412456, 6865748, 6923456, 6523405], False: [6023675, 6023594, 6725684, 6026485, 60273845, 6864850], None: [6323034, 6412456, 6865748, 6923456, 6523405, 6023675, 6023594, 6725684, 6026485, 60273845, 6864850]},
                     6: {True: [6712567, 6312567, 6621756, 6156034, 6923459, 6115693], False: [6334758, 6912847, 6512845, 6574839, 6023456], None: [6712567, 6312567, 6621756, 6156034, 6923459, 6115693, 6334758, 6912847, 6512845, 6574839, 6023456]},
                     7: {True: [6323678, 6502345, 6702347, 6702345, 6546575, 6334567], False: [6012567, 6684576, 6112678, 6586576], None: [6323678, 6502345, 6702347, 6702345, 6546575, 6334567, 6012567, 6684576, 6112678, 6586576]}}
    prices_av = {1: [409354, 403823, 473832, 483405, 493574, 402384, 406374],
                      2: [43862, 404738, 404345, 434748, 435975, 412856, 448435, 402346],
                      3: {True: [422345, 492465, 431457, 472345], False: [412465, 402485, 481734, 444263, 466237, 412839], None: [422345, 492465, 431457, 472345, 412465, 402485, 481734, 444263, 466237, 412839]},
                      4: {True: [430123, 434567, 436344, 433576, 452569, 492485, 416045], False: [441574, 455483, 422457, 402345, 416758], None: [430123, 434567, 436344, 433576, 452569, 492485, 416045, 441574, 455483, 422457, 402345, 416758]},
                      5: {True: [490234, 445758, 402456, 445684, 402345], False: [400000, 437849, 425783, 402384, 423458], None: [490234, 445758, 402456, 445684, 402345, 400000, 437849, 425783, 402384, 423458]}}
    prices_p = {1: [220465, 214867, 206758, 227485, 204596, 234569, 246578, 223647, 247685, 234566],
                     2: [245968, 245633, 204507, 224578, 202345, 245364, 204067, 224507, 204560, 223475, 284507, 204507]}
    addition_r = {'electric_oven': 50040, 'furniture_pack': 125700, 'parking_space': 509400}
    addition_av = {'electric_oven': 35700, 'furniture_pack': 69500, 'parking_space': 253800}

    def __init__(self, budget: int, floor: int|None, OptionsPrice: int|None, balcony: bool|None) -> None:
        self.budget = budget
        self.floor = floor
        self.OptionsPrice = OptionsPrice
        self.balcony = balcony

    #create an instance of the class
    @classmethod
    def expensive(cls, budget, floor, furniture_pack, parking_space, balcony) -> 'INSTANCE of three_houses_district':
        # Calculate additional options price based on selection
        OptionsPrice = sum((cls.addition_r['electric_oven'], cls.addition_r['furniture_pack'] if furniture_pack else 0, cls.addition_r['parking_space'] if parking_space else 0))
        return cls(budget, floor, OptionsPrice, balcony)

    # create an instance of the class
    @classmethod
    def average(cls, budget, floor, electric_oven, furniture_pack, balcony) -> 'INSTANCE of three_houses_district':
        # Calculate additional options price based on selection
        OptionsPrice = sum((cls.addition_av['electric_oven'] if electric_oven else 0, cls.addition_av['furniture_pack'] if furniture_pack else 0))
        return cls(budget, floor, OptionsPrice, balcony)

    # create an instance of the class
    @classmethod
    def cheap(cls, budget, floor) -> 'INSTANCE of three_houses_district':
        return cls(budget, floor, None, False)

    #calculate the result
    def expensive_house(self) -> str:
        if self.floor is None:
            return f'<<<YOUR BUDGET - {self.budget}>>>\n' + self.flNone(self.prices_r)
        return f'<<<YOUR BUDGET - {self.budget}>>>\n' + self.fl(self.prices_r)

    # calculate the result
    def average_house(self) -> str:
        if self.floor is None:
            return f'<<<YOUR BUDGET - {self.budget}>>>\n' + self.flNone(self.prices_av)
        return f'<<<YOUR BUDGET - {self.budget}>>>\n' + self.fl(self.prices_av)

    # calculate the result
    def cheap_house(self) -> str:
        if self.floor is None:
            sp = [[f, list(map(str, sorted(filter(lambda x: x <= self.budget, self.prices_p[f]))))] for f in range(1, len(self.prices_p) + 1)]
            return f'<<<YOUR BUDGET - {self.budget}>>>\n' + '\n'.join([f'{len(ap)} appartment{"" if len(ap) == 1 else "s"} available on the {f} floor:\n<prices: {", ".join(ap)}>\n' for f, ap in sp])

        sp = [self.floor, list(map(str, sorted(filter(lambda x: x <= self.budget, self.prices_p[self.floor]))))]
        return f'<<<YOUR BUDGET - {self.budget}>>>\n' + f'{len(sp[1])} appartment{"" if len(sp[1]) == 1 else "s"} available on the {sp[0]} floor:\n<prices: {", ".join(sp[1])}>\n'

    def flNone(self, sl: dict):
        sp = [[f, list(map(str, sorted(filter(lambda x: x <= self.budget, map(lambda x: x + self.OptionsPrice,
                                                                      sl[f] if len(sl[f]) != 3 
                                                                      else sl[f][self.balcony])))))] for f in range(1, len(sl) + 1)]
        return '\n'.join([f'{len(ap)} appartment{"" if len(ap) == 1 else "s"} available on the {f} floor:\n<prices: {", ".join(ap)}>\n' for f, ap in sp])

    def fl(self, sl: dict):
        sp = [self.floor, list(map(str, sorted(filter(lambda x: x <= self.budget, map(lambda x: x + self.OptionsPrice,
                                                                      sl[self.floor] if len(sl[self.floor]) != 3 
                                                                      else sl[self.floor][self.balcony])))))]
        return f'{len(sp[1])} appartment{"" if len(sp[1]) == 1 else "s"} available on the {sp[0]} floor:\n<prices: {", ".join(sp[1])}>\n'







