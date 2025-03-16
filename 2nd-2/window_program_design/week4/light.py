from tkinter import *
import threading
import time

from enum import Enum

class TrafficLight:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Light")
        self.root.geometry("402x102")
        
        # 初始化畫布
        self.canvas = Canvas(root, width=400, height=100)
        self.canvas.pack()
        
        # 設置尺寸和位置
        self.size = 100
        self.y0 = 50
        self.y1 = self.y0 - self.size/2
        self.y2 = self.y0 + self.size/2
        
        # 紅燈閃爍控制
        self.red_positions = [0, 100]  # 紅燈的兩個位置
        self.current_red_index = 0  # 目前紅燈位置的索引
        
        # 燈號位置
        self.positions = {
            'yellow': 200,
            'green': 300
        }
        
        # 燈號時間（秒）
        self.timings = {
            'red': 5,
            'yellow': 1.5,
            'green': 3
        }
        
        self.running = True
        
    def draw_circle(self, x, color):
        """繪製指定顏色的圓"""
        self.canvas.create_oval(x, self.y1, x + self.size, self.y2, 
                              fill=color, outline="")
    
    def draw_traffic_state(self, active_light):
        """繪製交通燈狀態"""
        self.canvas.delete("all")
        
        # 特殊處理紅燈的閃爍
        if active_light == 'red':
            # 在兩個位置畫黑圓
            self.draw_circle(0, "black")
            self.draw_circle(100, "black")
            # 在當前位置畫紅圓
            self.draw_circle(self.red_positions[self.current_red_index], 'red')
        else:
            # 非紅燈時重置紅燈位置
            self.current_red_index = 0
            self.draw_circle(0, "black")
            self.draw_circle(100, "black")
        
        # 繪製黃燈和綠燈
        self.draw_circle(200, "yellow" if active_light == "yellow" else "black")
        self.draw_circle(300, "green" if active_light == "green" else "black")
    
    def control_cycle(self):
        """控制交通燈循環"""
        while self.running:
            # 紅燈特殊處理
            start_time = time.time()
            while time.time() - start_time < self.timings['red'] and self.running:
                self.draw_traffic_state('red')
                time.sleep(0.5)  # 控制閃爍頻率
                self.current_red_index = (self.current_red_index + 1) % 2  # 切換紅燈位置
            
            if not self.running:
                break
                
            # 黃燈和綠燈正常處理
            for light in ['yellow', 'green']:
                self.draw_traffic_state(light)
                time.sleep(self.timings[light])
                if not self.running:
                    break
    
    def start(self):
        """啟動交通燈"""
        control_thread = threading.Thread(target=self.control_cycle)
        control_thread.daemon = True
        control_thread.start()
    
    def stop(self):
        """停止交通燈"""
        self.running = False
        self.root.destroy()

def main():
    root = Tk()
    traffic_light = TrafficLight(root)
    traffic_light.start()
    
    # 設置關閉視窗的處理
    root.protocol("WM_DELETE_WINDOW", traffic_light.stop)
    root.mainloop()

if __name__ == "__main__":
    main()