import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Extract data',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32, np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.to_start = 0  # count to start
        self.to_end = 0  # count to end
        '''state
            1 when estimated preamble, prepare to start
            2 when estimated postamble, prepare to stop
            3 when info data is transmitting
            0 otherwise'''
        self.state = 0

    def work(self, input_items, output_items):
        for smapleIndex in range(len(input_items[0])):
            # detect tag
            tags = self.get_tags_in_window(0, smapleIndex, smapleIndex+1)  # get the tags
            for tag in tags:
                key = pmt.to_python(tag.key)
                if key != 'corr_est':  # only to find tag "corr_est"
                    continue
                else:
                    value = pmt.to_python(tag.value)
                    if (round(value)==169) and (self.state==0):  # preamble
                        self.state = 1
                        self.to_start = 13
                    elif (round(value)==121) and (self.state==3):  # postamble
                        self.state = 2
                        self.to_end = 11
                    break
            
            # do
            output_items[1][smapleIndex] = None
            if self.state == 3:  # transmitting
                output_items[1][smapleIndex] = input_items[0][smapleIndex]  # data to port 1
            elif self.state == 1:  # prepare to start
                self.to_start -= 1
            elif self.state == 2:  # prepare to stop
                self.to_end -= 1
            
            # state update
            if (self.state==1) and (self.to_start==0):  # data start at next sample
                self.state = 3
            elif (self.state==2) and (self.to_end==0):  # end and stop
                self.state = 0

        output_items[0][:] = input_items[0]  # copy all samples to output port 0
        return len(output_items[0])
