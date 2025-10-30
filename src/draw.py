import matplotlib.pyplot as plt
import numpy as np

# hàm vẽ đồ thị theo hàm tham số x=f(t), y=g(t)
def plot_parametric_trajectory(x_func, y_func, t_start, t_end, num_points=500, label=None):
    t = np.linspace(t_start, t_end, num_points)
    x_values = [x_func.subs('t', val) for val in t]
    y_values = [y_func.subs('t', val) for val in t]
    plt.plot(x_values, y_values, label=label)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    # Hiển thị lưới và chú thích
    plt.grid(True)
    plt.legend()