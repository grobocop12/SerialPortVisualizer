import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import os

global x_axis, y_axis, interval, time_span, axes, serial_port, line
interval = 10
x_axis, y_axis = np.reshape(np.arange(-300, 0, 1), 300), np.zeros(300)

time_span = 0


def main():
    global axes, serial_port
    device_file = get_device_file()
    serial_port = open_serial_port(device_file)
    figure = create_chart_figure()
    figure, axes = add_axes(figure)
    visualize_data(figure)
    close_serial_port(serial_port)


def animate(i):
    global axes, x_axis, y_axis, serial_port, interval, time_span, line

    byte = read_byte_of_data(serial_port)
    data = byte_to_signed_int(byte)

    y_axis[:-1] = y_axis[1:]
    y_axis[-1] = data
    time_span += interval



    line.set_ydata(y_axis)
    return line,


def cut_axis_to_limit(axis):
    if len(axis) > 30:
        return axis[-30::]
    else:
        return axis


def init():
    global line, y_axis
    line.set_ydata(y_axis)
    return line,


def visualize_data(figure):
    global interval, axes, line, x_axis, y_axis
    line, = axes.plot(x_axis, y_axis)
    graph_animation = animation.FuncAnimation(figure, animate, interval=interval, init_func=init, blit=True)
    plt.ylim(-6, 6)
    plt.show()


def byte_to_signed_int(byte):
    return int.from_bytes(byte, byteorder='big', signed=True)


def read_byte_of_data(port):
    byte = port.read(1)
    return byte


def add_axes(figure):
    ax = figure.add_subplot(1, 1, 1)
    return figure, ax


def create_chart_figure():
    figure = plt.figure()
    return figure


def close_serial_port(closing_port):
    closing_port.close()
    return closing_port


def open_serial_port(device_file):
    opened_port = serial.Serial(device_file)
    return opened_port


def get_device_file():
    try:
        device_file = read_standard_input()
        if not file_exist(device_file):
            print_error_message_and_exit("File %s does not exist." % device_file)
        return device_file
    except IndexError:
        print_error_message_and_exit("Not enough input arguments.")


def print_error_message_and_exit(error_message):
    print(error_message)
    print_help()
    exit(-1)


def print_help():
    print('Example usage:\npython reader.py <path to device file>')


def file_exist(device_file):
    return os.path.exists(device_file)


def read_standard_input():
    return sys.argv[1]


if __name__ == '__main__':
    main()
