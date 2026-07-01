import sys, math, random, os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QPen, QPolygonF

class MotismaMecha(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(160, 160)

        screen = QApplication.primaryScreen().geometry()
        self.sw, self.sh = screen.width(), screen.height()
        self.x, self.y = float(self.sw/2), float(self.sh/2)
        self.vx, self.vy = 0.0, 0.0
        self.friction = 0.94
        
        self.status = "listening" 
        self.pulse = 0.0
        self.eye_blink = 0
        self.current_angle = random.uniform(0, 6.28)
        self.is_panicking = False
        self.last_m_pos = self.cursor().pos()

        self.timer = QTimer()
        self.timer.timeout.connect(self.engine)
        self.timer.start(16)

        self.dir_timer = QTimer()
        self.dir_timer.timeout.connect(self.change_direction)
        self.dir_timer.start(5000)


        with open("status.txt", "w") as f: f.write("listening")

    def change_direction(self):
        if not self.is_panicking:
            self.current_angle = random.uniform(0, 6.28)

    def engine(self):

        try:
            if os.path.exists("status.txt"):
                with open("status.txt", "r") as f: 
                    self.status = f.read().strip()
            else:
                self.status = "listening"
        except: pass

        m_pos = self.cursor().pos()
        dx, dy = (self.x + 80) - m_pos.x(), (self.y + 80) - m_pos.y()
        dist = math.sqrt(dx**2 + dy**2)
        m_speed = math.sqrt((m_pos.x() - self.last_m_pos.x())**2 + (m_pos.y() - self.last_m_pos.y())**2)

        if dist < 140:
            force = 9.0 if m_speed > 12 else 2.5
            self.vx += (dx/dist) * force * ((140-dist)/140)
            self.is_panicking = (m_speed > 12)
        else:
            self.is_panicking = False
            self.vx += math.cos(self.current_angle) * 0.04
            self.vy += math.sin(self.current_angle) * 0.04

        self.last_m_pos = m_pos
        self.vx *= self.friction ; self.vy *= self.friction
        self.x += self.vx ; self.y += self.vy

        if self.x < 0 or self.x > self.sw-160: self.vx *= -1.5 ; self.change_direction()
        if self.y < 0 or self.y > self.sh-160: self.vy *= -1.5 ; self.change_direction()

        self.x = max(0, min(self.x, self.sw-160))
        self.y = max(0, min(self.y, self.sh-160))
        
        self.pulse += 0.15
        if self.eye_blink > 0: self.eye_blink -= 1
        elif random.random() < 0.01: self.eye_blink = 12

        self.move(int(self.x), int(self.y))
        self.update()

    def draw_face(self, painter, center):
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.PenStyle.NoPen)
        eye_h = 12 if self.eye_blink == 0 else 2
        
        m_pos = self.cursor().pos()
        lx = max(-5, min(5, (m_pos.x() - self.x - 80) / 20))
        ly = max(-5, min(5, (m_pos.y() - self.y - 80) / 20))
        
        painter.drawEllipse(QPointF(center - 12 + lx, center - 5 + ly), 4, eye_h/2)
        painter.drawEllipse(QPointF(center + 12 + lx, center - 5 + ly), 4, eye_h/2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = 80
        
        colors = {
            "listening": QColor(255, 140, 0), 
            "thinking": QColor(0, 180, 255), 
            "speaking": QColor(0, 255, 120), 
            "error": QColor(255, 0, 0)
        }
        
        c = QColor(255,255,255) if self.is_panicking else colors.get(self.status, colors["listening"])

        painter.setPen(QPen(c, 2))
        painter.setBrush(QColor(c.red(), c.green(), c.blue(), 40))

        if self.status == "speaking": 
            for i in range(3):
                a = self.pulse * 5 + i * 2.09
                p = QPointF(center + math.cos(a)*55, center + math.sin(a)*55)
                painter.drawLine(QPointF(center, center), p)
                painter.drawEllipse(p, 10, 10)
        elif self.status == "thinking": 
            s = 45 + math.sin(self.pulse*2)*5
            painter.drawRect(QRectF(center-s/2, center-s/2, s, s))
            for i in range(4):
                a = self.pulse + i * 1.57
                painter.drawEllipse(QPointF(center + math.cos(a)*28, center + math.sin(a)*28), 4, 4)
        else: 
            painter.drawEllipse(QPointF(center, center), 35, 35)
            for i in [-1, 1]:
                a = -1.57 + (i * 0.8) + math.sin(self.pulse)*0.2
                p2 = QPointF(center + math.cos(a)*65, center + math.sin(a)*65)
                painter.drawLine(QPointF(center + math.cos(a)*35, center + math.sin(a)*35), p2)
                painter.drawEllipse(p2, 3, 3)

        grad = QRadialGradient(center, center, 25)
        grad.setColorAt(0, c)
        grad.setColorAt(1, QColor(c.red(), c.green(), c.blue(), 100))
        painter.setBrush(grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(center, center), 25, 25)
        self.draw_face(painter, center)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    orb = MotismaMecha()
    orb.show()
    sys.exit(app.exec())
