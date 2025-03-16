import tkinter as tk

class PacMan:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pac-Man")
        
        # 創建黑色背景的畫布
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='black')
        self.canvas.pack()
        
        # 初始化參數
        self.mouth_angle = 0     # 嘴巴角度
        self.opening = True      # 控制開合方向
        
        self.animate()
        self.root.mainloop()
    
    def animate(self):
        # 清除畫布
        self.canvas.delete('all')
        
        # 繪製 Pac-Man
        self.canvas.create_arc(
            50, 50, 250, 250,    # 位置和大小
            start=self.mouth_angle,  # 開始角度
            extent=360 - self.mouth_angle * 2,  # 圓弧範圍
            fill='yellow'        # Pac-Man 的黃色
        )
        
        # 更新嘴巴角度
        if self.opening:
            self.mouth_angle += 2
            if self.mouth_angle >= 45:  # 最大張開角度
                self.opening = False
        else:
            self.mouth_angle -= 2
            if self.mouth_angle <= 0:   # 完全閉合
                self.opening = True
        
        # 設定下一幀
        self.root.after(10, self.animate)

# 執行動畫
if __name__ == "__main__":
    pacman = PacMan()
