from collections import OrderedDict

SIDES = OrderedDict([('U', 0), ('F', 1), ('R', 2), ('D', 3), ('B', 4), ('L', 5)])
SIDES_VECTORS = ((0, 1, 0), (0, 0, 1), (1, 0, 0), (0, -1, 0), (0, 0, -1), (-1, 0, 0))


class Block(object):
    def __init__(self, coord, parent=None, parent_side: int = None):
        """
        Up = 0 Front = 1 Right = 2; opposite side is +3
        :param coord: tuple(x, y, z) of 3d position
        :param parent: Block object
        :param parent_side: the child_side from within the parent to get to this object.
                            To access parent_side from within this object use the inverse.
        """
        self.coord = coord
        self.sides = [None] * len(SIDES)
        self.parent_side = None
        self.child_side = None
        if 0 <= (parent_side if parent_side is not None else -1) < len(self.sides) and isinstance(parent, Block):
            self.parent_side = (parent_side + 3) % 6
            self.sides[self.parent_side] = parent
            parent.set_child(self, parent_side)

    def set_child(self, child, child_side):
        if 0 <= (child_side if child_side is not None else -1) < len(self.sides) and isinstance(child, Block):
            self.child_side = child_side
            self.sides[child_side] = child

    def get_rotation(self):
        """
        :return: strings indicating possible rotations available else None
        """
        if self.parent_side is None or self.child_side is None or ((self.parent_side - self.child_side) % 3 == 0):
            # if connections on opposite sides or no parent or no child, then can't rotate
            return None
        ps = [list(SIDES)[self.parent_side], list(SIDES)[(self.parent_side + 3) % 6]]
        cs = [list(SIDES)[self.child_side], list(SIDES)[(self.child_side + 3) % 6]]
        return ''.join(set(SIDES) - set(ps)) + ' & ' + ''.join(set(SIDES) - set(cs))


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
                    self.blocks.append(Block(coord=(0, 0, 0)))
                elif line not in SIDES:
                    raise ValueError(f'Direction "{line}" is invalid. Expecting: {", ".join(list(SIDES))}')
                else:
                    self.blocks.append(Block(
                        coord=tuple(sum(x) for x in zip(self.blocks[idx-1].coord, SIDES_VECTORS[SIDES[line]])),
                        parent=self.blocks[idx-1],
                        parent_side=SIDES[line]
                    ))
                idx += 1
        if idx == 0:
            raise ValueError('Start of sequence must begin with "S", which was not found')

    def print_shape(self):
        side = None
        for b in self.blocks:
            print(f'{list(SIDES)[side] if side is not None else "S"} {str(b.coord)} {b.get_rotation()}')
            side = b.child_side


if __name__ == '__main__':
    c = Chain()
    c.load_shape('shape.txt')
    c.print_shape()
