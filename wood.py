from collections import OrderedDict

SIDES = OrderedDict([('U', 0), ('F', 1), ('R', 2), ('D', 3), ('B', 4), ('L', 5)])
SIDES_VECTORS = ((0, 1, 0), (0, 0, 1), (1, 0, 0), (0, -1, 0), (0, 0, -1), (-1, 0, 0))


class Block(object):
    def __init__(self, coord, parent=None, parent_side=None):
        """
        Up = 0 Front = 1 Right = 2; opposite side is +3
        """
        self.coord = coord
        self.sides = [None] * len(SIDES)
        self.parent_side = None
        self.child_side = None
        if 0 <= (parent_side if parent_side is not None else -1) < len(self.sides) and isinstance(parent, Block):
            self.parent_side = int(parent_side)
            self.sides[parent_side] = parent
            parent.set_child(self, (parent_side + 3) % 6)

    def set_child(self, child, child_side):
        if 0 <= (child_side if child_side is not None else -1) < len(self.sides) and isinstance(child, Block):
            self.child_side = child_side
            self.sides[child_side] = child


class Chain(object):
    def __init__(self):
        self.blocks = []

    def load_shape(self, fname):
        idx = 0
        with open(fname) as fin:
            for line in fin:
                line = line.replace('\n', '')
                if idx == 0 and line != 'S':
                    idx -= 1
                elif idx == 0 and line == 'S':
                    self.blocks.append(Block((0, 0, 0)))
                elif line not in SIDES:
                    raise ValueError(f'Direction "{line}" is invalid. Expecting: {", ".join(list(SIDES))}')
                else:
                    self.blocks.append(Block(
                        tuple(sum(x) for x in zip(self.blocks[idx-1].coord, SIDES_VECTORS[SIDES[line]])),
                        self.blocks[idx-1],
                        (SIDES[line] + 3) % 6
                    ))
                idx += 1
        if idx == 0:
            raise ValueError('Start of sequence must begin with "S", which was not found')

    def print_shape(self):
        side = None
        for b in self.blocks:
            print(f'{list(SIDES)[side] if side else "S"} {str(b.coord)}')
            side = b.child_side


if __name__ == '__main__':
    c = Chain()
    c.load_shape('shape.txt')
    c.print_shape()
