"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, down_th=-0.5, up_th=0.5, default_out=0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Threshold',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.down_th = down_th
        self.up_th = up_th
        self.default_out = default_out

    def work(self, input_items, output_items):
        for smapleIndex in range(len(input_items[0])):
            if input_items[0][smapleIndex] <= self.down_th:
                output_items[0][smapleIndex] = -1.0
            elif input_items[0][smapleIndex] >= self.up_th:
                output_items[0][smapleIndex] = 1.0
            else:
                output_items[0][smapleIndex] = self.default_out

        return len(output_items[0])
