import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sympy as sp

def ve_do_thi(above,bottom):
    fig = plt.figure(figsize=(10, 8))

    # Define the grid and create the subplots (axes)
    ax1 = plt.subplot2grid((2, 3), (0, 0))
    ax2 = plt.subplot2grid((2, 3), (0, 1))
    ax3 = plt.subplot2grid((2, 3), (0, 2))
    
    total_frames = 200
    
    vantoc = above["vantoc"]
    phaptuyen = above["phaptuyen"]
    tieptuyen = above["tieptuyen"]
    
    gocnem1 = bottom["gocnem1"]
    gocnem2 = bottom["gocnem2"]

    t = sp.symbols("t")
    time = np.linspace(0, gocnem2["t"], total_frames)
    
    vantoc_num = sp.lambdify(t,vantoc, "numpy");
    phaptuyen_num = sp.lambdify(t,phaptuyen, "numpy");
    tieptuyen_num = sp.lambdify(t,tieptuyen, "numpy");

    vantoc_full =vantoc_num(time)
    phaptuyen_full =phaptuyen_num(time)
    tieptuyen_full =tieptuyen_num(time)
    
    ax1.set_xlim(0, gocnem2["t"] * 1.1)
    ax1.set_ylim(0, np.max(vantoc_full) * 1.1)
    ax1.set_title("Vận tốc theo thời gian")
    ax1.set_xlabel("Thời gian (s)")
    ax1.set_ylabel("Vận Tốc")
    ax1.grid(True)

    ax2.set_xlim(0, gocnem2["t"] * 1.1)
    ax2.set_ylim(0, np.max(phaptuyen_full) * 1.1)
    ax2.set_title("Gia tốc hướng tâm theo thời gian")
    ax2.set_xlabel("Thời gian (s)")
    ax2.set_ylabel("Gia tốc hướng tâm (m/s²)")
    ax2.grid(True)


    ax3.set_xlim(0, gocnem2["t"] * 1.1)
    ax3.set_ylim(np.max(tieptuyen_full) * -1.1, np.max(tieptuyen_full) * 1.1)
    ax3.set_title("Gia tốc tiếp tuyến theo thời gian")
    ax3.set_xlabel("Thời gian (s)")
    ax3.set_ylabel("Gia tốc tiếp tuyến (m/s²)")
    ax3.grid(True)

    ax4 = plt.subplot2grid((2, 3), (1, 0), colspan=3)
    
    # Sử dụng lambdify để chuyển đổi biểu thức SymPy thành các hàm NumPy nhanh hơn
    t_sym = sp.Symbol('t')
    num_x1_func = sp.lambdify(t_sym, gocnem1["x"], 'numpy')
    num_y1_func = sp.lambdify(t_sym, gocnem1["y"], 'numpy')
    num_x2_func = sp.lambdify(t_sym, gocnem2["x"], 'numpy')
    num_y2_func = sp.lambdify(t_sym, gocnem2["y"], 'numpy')

    # Tính toán toàn bộ quỹ đạo để xác định giới hạn cho các trục
    t1_full = np.linspace(0, gocnem1["t"], 200)
    x1_full = num_x1_func(t1_full)
    y1_full = num_y1_func(t1_full)

    t2_full = np.linspace(0, gocnem2["t"], 200)
    x2_full = num_x2_func(t2_full)
    y2_full = num_y2_func(t2_full)

    # Đặt giới hạn cho trục x và y để chứa cả hai quỹ đạo (thêm 10% lề)
    ax4.set_xlim(0, np.max(x1_full) * 1.1)
    ax4.set_ylim(0, np.max([np.max(y1_full), np.max(y2_full)]) * 1.1)
    
    # Tạo hai đường đồ thị trống. Chúng ta sẽ cập nhật dữ liệu cho các đường này
    line4, = ax4.plot([], [], lw=2, label=f"Góc ném a1 = {gocnem1["a"]}°", color='blue')
    line5, = ax4.plot([], [], lw=2, label=f"Góc ném a2 = {gocnem2["a"]:.3f}°", color='red')
    ax4.grid()
    
    # Thiết lập các thông tin khác cho đồ thị
    ax4.set_xlabel('Tầm xa (m)')
    ax4.set_ylabel('Độ cao (m)')
    ax4.set_title('Hoạt ảnh quỹ đạo của vật với hai góc ném')
    ax4.grid(True)
    ax4.legend()

    line1, = ax1.plot([], [], lw=2,color="red")
    line2, = ax2.plot([], [], lw=2,color="red")
    line3, = ax3.plot([], [], lw=2,color="red")

    t_max = max(gocnem1["t"], gocnem2["t"]) # Hoạt ảnh sẽ chạy theo thời gian dài hơn

    lines = [line1, line2, line3, line4, line5]

    def init():
        for line in lines:
            line.set_data([], [])
        return lines
    
    def update(frame):
        line1.set_data(time[:frame], vantoc_full[:frame])
        line2.set_data(time[:frame], phaptuyen_full[:frame])
        line3.set_data(time[:frame], tieptuyen_full[:frame])
        
        # i là số khung hình, từ 0 đến frames-1
        # Chuyển đổi số khung hình i thành giá trị thời gian t hiện tại
        current_t = t_max * (frame / total_frames)
        
        # Cập nhật quỹ đạo 1
        if current_t <= gocnem1["t"]:
            t_values1 = np.linspace(0, current_t, 200)
        else: # Nếu đã bay xong, giữ nguyên ở cuối quỹ đạo
            t_values1 = np.linspace(0, gocnem1["t"], 200)
        
        x_values1 = num_x1_func(t_values1)
        y_values1 = num_y1_func(t_values1)
        line4.set_data(x_values1, y_values1)

        # Cập nhật quỹ đạo 2
        if current_t <= gocnem2["t"]:
            t_values2 = np.linspace(0, current_t, 200)
        else: # Nếu đã bay xong, giữ nguyên ở cuối quỹ đạo
            t_values2 = np.linspace(0, gocnem2["t"], 200)
            
        x_values2 = num_x2_func(t_values2)
        y_values2 = num_y2_func(t_values2)
        line5.set_data(x_values2, y_values2)

        # return line1, line2

        return lines
    
    animation.FuncAnimation(fig, update, frames=total_frames,init_func=init, blit=True, interval=30)

    plt.tight_layout()
    plt.show()