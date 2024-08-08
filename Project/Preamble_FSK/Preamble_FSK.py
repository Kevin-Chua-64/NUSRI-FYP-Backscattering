#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: simulated FSK preamble
# Author: Admin
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import Preamble_FSK_epy_block_0 as epy_block_0  # embedded python block
import Preamble_FSK_epy_block_1 as epy_block_1  # embedded python block
import Preamble_FSK_epy_block_2 as epy_block_2  # embedded python block
import random
import sip



class Preamble_FSK(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "simulated FSK preamble", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("simulated FSK preamble")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Preamble_FSK")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3200000
        self.freq = freq = 4000
        self.preamble = preamble = [+1,+1,+1,+1,+1,-1,-1,+1,+1,-1,+1,-1,+1]
        self.postamble = postamble = [+1,+1,+1,-1,-1,-1,+1,-1,-1,+1,-1]
        self.decim = decim = int(samp_rate/(8*freq))
        self.data = data = [random.choice((-1,1)) for i in range(16)]
        self.bit_rate = bit_rate = 1000
        self.preamble_label = preamble_label = preamble
        self.postamble_label = postamble_label = postamble
        self.pad = pad = int(samp_rate/bit_rate)
        self.noise = noise = 0.001
        self.low_pass = low_pass = firdes.low_pass(1.0, samp_rate, 1.5*freq,freq, window.WIN_HAMMING, 6.76)
        self.gain = gain = 0.8
        self.data_label = data_label = data
        self.GUI_t = GUI_t = 0.1
        self.FM_devia = FM_devia = 1
        self.FM_decim = FM_decim = int(samp_rate/decim/(bit_rate))

        ##################################################
        # Blocks
        ##################################################

        self._noise_range = Range(0.001, 0.01, 0.001, 0.001, 200)
        self._noise_win = RangeWidget(self._noise_range, self.set_noise, "'noise'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_win, 0, 2, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = Range(0.4, 2, 0.2, 0.8, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "'gain'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0_0 = qtgui.time_sink_f(
            (int(GUI_t*samp_rate/decim/FM_decim)), #size
            samp_rate/decim/FM_decim, #samp_rate
            'Data', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_2_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0_0.enable_grid(True)
        self.qtgui_time_sink_x_2_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_0_0_win, 4, 0, 1, 4)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_f(
            (int(GUI_t*samp_rate/decim/FM_decim)), #size
            samp_rate/decim/FM_decim, #samp_rate
            'Tagged', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0.set_y_axis(-1.5, 3)

        self.qtgui_time_sink_x_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(True)
        self.qtgui_time_sink_x_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_0_win, 3, 0, 1, 4)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            (int(GUI_t*samp_rate/decim/FM_decim)), #size
            samp_rate/decim/FM_decim, #samp_rate
            'FM Demod', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(True)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_2_win, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._preamble_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._preamble_label_formatter = None
        else:
            self._preamble_label_formatter = lambda x: repr(x)

        self._preamble_label_tool_bar.addWidget(Qt.QLabel("Preamble: "))
        self._preamble_label_label = Qt.QLabel(str(self._preamble_label_formatter(self.preamble_label)))
        self._preamble_label_tool_bar.addWidget(self._preamble_label_label)
        self.top_grid_layout.addWidget(self._preamble_label_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._postamble_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._postamble_label_formatter = None
        else:
            self._postamble_label_formatter = lambda x: repr(x)

        self._postamble_label_tool_bar.addWidget(Qt.QLabel("Postamble: "))
        self._postamble_label_label = Qt.QLabel(str(self._postamble_label_formatter(self.postamble_label)))
        self._postamble_label_tool_bar.addWidget(self._postamble_label_label)
        self.top_grid_layout.addWidget(self._postamble_label_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, low_pass, 0, samp_rate)
        self.epy_block_2 = epy_block_2.blk()
        self.epy_block_1 = epy_block_1.blk(down_th=-0.5, up_th=0.5, default_out=0.0)
        self.epy_block_0 = epy_block_0.blk()
        self.digital_corr_est_cc_0_0 = digital.corr_est_cc(postamble, 1, 1, 0.9, digital.THRESHOLD_ABSOLUTE)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(preamble, 1, 1, 0.9, digital.THRESHOLD_ABSOLUTE)
        self._data_label_tool_bar = Qt.QToolBar(self)

        if None:
            self._data_label_formatter = None
        else:
            self._data_label_formatter = lambda x: repr(x)

        self._data_label_tool_bar.addWidget(Qt.QLabel("Data: "))
        self._data_label_label = Qt.QLabel(str(self._data_label_formatter(self.data_label)))
        self._data_label_tool_bar.addWidget(self._data_label_label)
        self.top_grid_layout.addWidget(self._data_label_tool_bar, 2, 2, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_f(preamble+data+postamble, True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_float * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, pad)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(0.8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(gain)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc((-30), 1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (-freq), 1, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise, 0)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=(samp_rate/decim),
        	audio_decim=FM_decim,
        	deviation=(FM_devia*freq),
        	audio_pass=(0.1*freq),
        	audio_stop=(2*freq),
        	gain=1.0,
        	tau=0,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.epy_block_1, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.epy_block_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.epy_block_0, 2))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.epy_block_2, 0))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.qtgui_time_sink_x_2_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_corr_est_cc_0_0, 0))
        self.connect((self.digital_corr_est_cc_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.epy_block_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.epy_block_1, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.epy_block_2, 1), (self.blocks_tag_gate_0, 0))
        self.connect((self.epy_block_2, 0), (self.qtgui_time_sink_x_2_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_simple_squelch_cc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Preamble_FSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_FM_decim(int(self.samp_rate/self.decim/(self.bit_rate)))
        self.set_decim(int(self.samp_rate/(8*self.freq)))
        self.set_low_pass(firdes.low_pass(1.0, self.samp_rate, 1.5*self.freq, self.freq, window.WIN_HAMMING, 6.76))
        self.set_pad(int(self.samp_rate/self.bit_rate))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_decim(int(self.samp_rate/(8*self.freq)))
        self.set_low_pass(firdes.low_pass(1.0, self.samp_rate, 1.5*self.freq, self.freq, window.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_frequency((-self.freq))
        self.analog_sig_source_x_0_0.set_frequency(self.freq)

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.set_preamble_label(self.preamble)
        self.blocks_vector_source_x_0.set_data(self.preamble+self.data+self.postamble, [])

    def get_postamble(self):
        return self.postamble

    def set_postamble(self, postamble):
        self.postamble = postamble
        self.set_postamble_label(self.postamble)
        self.blocks_vector_source_x_0.set_data(self.preamble+self.data+self.postamble, [])

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_FM_decim(int(self.samp_rate/self.decim/(self.bit_rate)))
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.set_data_label(self.data)
        self.blocks_vector_source_x_0.set_data(self.preamble+self.data+self.postamble, [])

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_FM_decim(int(self.samp_rate/self.decim/(self.bit_rate)))
        self.set_pad(int(self.samp_rate/self.bit_rate))

    def get_preamble_label(self):
        return self.preamble_label

    def set_preamble_label(self, preamble_label):
        self.preamble_label = preamble_label
        Qt.QMetaObject.invokeMethod(self._preamble_label_label, "setText", Qt.Q_ARG("QString", str(self._preamble_label_formatter(self.preamble_label))))

    def get_postamble_label(self):
        return self.postamble_label

    def set_postamble_label(self, postamble_label):
        self.postamble_label = postamble_label
        Qt.QMetaObject.invokeMethod(self._postamble_label_label, "setText", Qt.Q_ARG("QString", str(self._postamble_label_formatter(self.postamble_label))))

    def get_pad(self):
        return self.pad

    def set_pad(self, pad):
        self.pad = pad
        self.blocks_repeat_0.set_interpolation(self.pad)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_low_pass(self):
        return self.low_pass

    def set_low_pass(self, low_pass):
        self.low_pass = low_pass
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.low_pass)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.blocks_multiply_const_vxx_0.set_k(self.gain)

    def get_data_label(self):
        return self.data_label

    def set_data_label(self, data_label):
        self.data_label = data_label
        Qt.QMetaObject.invokeMethod(self._data_label_label, "setText", Qt.Q_ARG("QString", str(self._data_label_formatter(self.data_label))))

    def get_GUI_t(self):
        return self.GUI_t

    def set_GUI_t(self, GUI_t):
        self.GUI_t = GUI_t

    def get_FM_devia(self):
        return self.FM_devia

    def set_FM_devia(self, FM_devia):
        self.FM_devia = FM_devia

    def get_FM_decim(self):
        return self.FM_decim

    def set_FM_decim(self, FM_decim):
        self.FM_decim = FM_decim
        self.qtgui_time_sink_x_2.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)
        self.qtgui_time_sink_x_2_0_0.set_samp_rate(self.samp_rate/self.decim/self.FM_decim)




def main(top_block_cls=Preamble_FSK, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
