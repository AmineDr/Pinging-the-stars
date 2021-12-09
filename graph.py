from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from tkinter import ttk, Label


class GraphPage(ttk.Frame):
    def __init__(self, parent, nb_points):
        ttk.Frame.__init__(self, parent)
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.figure.patch.set_facecolor('#f0f0f0')
        self.ax = self.figure.add_subplot(111)
        self.parent = parent
        myFmt = mdates.DateFormatter("%H:%M:%S")
        self.ax.xaxis.set_major_formatter(myFmt)

        dateTimeObj = datetime.now() + timedelta(seconds=-nb_points)
        self.x_data = [dateTimeObj + timedelta(seconds=i) for i in range(nb_points)]
        self.y_data = [0 for i in range(nb_points)]

        self.plot = self.ax.plot(self.x_data, self.y_data, label='Ping')[0]
        self.ax.set_ylim(-10, 100)
        self.ax.set_xlim(self.x_data[0], self.x_data[-1])

        label = Label(self, text="Live latency plotting")
        label.pack()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

    def animate(self):
        self.x_data.append(datetime.now())
        try:
            self.y_data.append(self.parent.pings[-1])
            self.x_data = self.x_data[1:]
            self.y_data = self.y_data[1:]
            self.plot.set_xdata(self.x_data)
            self.plot.set_ydata(self.y_data)
            maximum = max(self.y_data)
            if maximum > 10:
                self.ax.set_ylim(-10, maximum)
            else:
                self.ax.set_ylim(-10, 10)
            self.ax.set_xlim(self.x_data[0], self.x_data[-1])
            self.canvas.draw_idle()
            if self.parent.pinging:
                self.after(self.parent.refreshRate, self.animate)
            else:
                self.ax.clear()
        except IndexError:
            pass