# Radar_instrument

This repository contains the necessary resources to build the radar instrument using a Raspberry Pi.

To download via command-line: ``` git clone https://www.github.com/deslay1/radar_instrument ```

Instrument design can be found in stl_files_to_3d_print.zip.

## Setting up the streaming server
To start receiving detection data from connected radar sensors, a streaming server has to be set up. The server is inside the directory called **rpi_xc112** and to run it, enter the following command from the current directory in the terminal:
``` ./rpi_xc112/utils/acc_streaming_server_rpi_xc112_r2b_xr112_r2b_a111_r2c ```

## Executing the main program
It is important to first download and install some required dependencies. This can be done by running the following command:
```python3.6 -m pip install -U --user -r requirements.txt```

To start playing the instrument, run the following command:
```python3.6 radar.py -s localhost --sensor 1 2```

## References
Upon encountering any issues, we would like to suggest visiting Acconeer, the company responsible for the project's radar sensors and software development kit. More specifically, we suggest visiting their Github repository (https://github.com/acconeer/acconeer-python-exploration) that contains a lot of information, guides and examples about configuring their radar sensors. 




