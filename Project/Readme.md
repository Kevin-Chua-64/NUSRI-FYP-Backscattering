# Project directory

+ **Project/**
  + **Matching_network/** -------- // **Simulated matching network of ADG701**
    + Matching_network_series_L_parallel_C.asc -------- // LTspice project file
    + Matching_network_series_L_parallel_C.log
    + Matching_network_series_L_parallel_C.op.raw
    + Matching_network_series_L_parallel_C.raw
    + Matching_network_series_L_parallel_C.txt -------- // The exported S11 data
    + Series_L_3nH_Parallel_C_12pF.jpg -------- // Smith chart
    + Smith_matching_network_series_L_parallel_C.py -------- // Plot the Smith chart
  + **No_bias_FSK/** -------- // **Processing by Python**
    + **Arduino/** -------- // **Arduino file**
      + **Arduino_BER/**
        + Arduino_BER.ino -------- // Send PN7 to test BER
      + **Arduino_simple/**
        + Arduino_simple.ino -------- // Send the data with preamble
    + **Pluto_scattered_FSK_filesink/** -------- // **Flowgraph for in GNU Radio**
      + Pluto_Rx.bin -------- // Received signal data
      + Pluto_scattered_filesink.grc -------- // GNU Radio project file
      + Pluto_scattered_filesink.py -------- // Generated Python file from GNU to run the flowgraph
      + **__pycache__/**
        + Pluto_scattered_FSK_filesink_epy_block_1.cpython-310.pyc
    + **Postprocess/** -------- // **Files for analyzing, running, and postprocessing**
      + **BER/** -------- // **Keep receiving to test BER**
        + FM_demod_BER.py -------- // Signal processing
        + Pluto_Rx.bin -------- // Received signal
        + Pluto_runRx_BER.py -------- // Run Pluto Rx
        + Pluto_runTx.py -------- // Run Pluto Tx
        + Run_BER.bat -------- // Top file for receving and processing
      + BER_SNR.py -------- // Plot theoretical BER
      + Display_file.py -------- // Display the .bin signal file
      + Extended_Hamming.py -------- // Generate Hamming matrix
      + FFT.py -------- // FFT of the signal
      + LFSR.py -------- // Generate PN7
      + Pluto_runTxRx.py -------- // Run Pluto Tx and Rx
      + **Realtime/** -------- // **Overall system**
        + FM_demod_UDP.py -------- // Singal processing
        + GUI.py -------- // GUI
        + Pluto_Rx.bin -------- // Received signal
        + Pluto_runRx.py -------- // Run Pluto Rx
        + Pluto_runTx.py -------- // Run Pluto Tx
        + Run.bat -------- // Top file for receiving, processing, and displaying
      + UDP_client.py -------- // Send UDP packet
      + UDP_server.py -------- // Bind the UDP port
  + **Pluto_scattered_FSK/** -------- // **Process in GNU Radio**
    + Display_file.py -------- // Display the .bin signal file
    + FSK_Demod.bin -------- // Received signal
    + Pluto_scattered_FSK.grc -------- // GNU Radio project file
    + Pluto_scattered_FSK.py -------- // Generated Python file from GNU to run the flowgraph
    + Pluto_scattered_FSK_epy_block_0.py
    + Pluto_scattered_FSK_epy_block_1.py
    + Pluto_scattered_FSK_epy_block_2.py
    + **__pycache__/**
      + Pluto_scattered_FSK_epy_block_0.cpython-310.pyc
      + Pluto_scattered_FSK_epy_block_1.cpython-310.pyc
      + Pluto_scattered_FSK_epy_block_2.cpython-310.pyc
  + **Preamble_FSK/** -------- // **Simulated FSK in GNU Radio**
    + Preamble_FSK.grc -------- // GNU Radio project file
    + Preamble_FSK.py -------- // Generated Python file from GNU to run the flowgraph
    + Preamble_FSK_epy_block_0.py
    + Preamble_FSK_epy_block_1.py
    + Preamble_FSK_epy_block_2.py
    + **__pycache__/**
      + Preamble_FSK_epy_block_0.cpython-310.pyc
      + Preamble_FSK_epy_block_1.cpython-310.pyc
      + Preamble_FSK_epy_block_2.cpython-310.pyc
      + Preamble_FSK_epy_block_3.cpython-310.pyc
  + Readme.md
