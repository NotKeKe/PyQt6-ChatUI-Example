from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QScrollArea, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from typing import Literal

MESSAGES = []

class ChatMessageWidget(QWidget):
    """
    一個自訂的聊天訊息元件，包含頭像、名稱和內文。
    """
    def __init__(self, name: str, content: str, avatar_path: str | None = None):
        super().__init__()

        # 1. 建立頭像 QLabel
        self.avatar_label = QLabel() 
        self.avatar_label.setFixedSize(40, 40)

        if avatar_path:
            pixmap = QPixmap(avatar_path)
            self.avatar_label.setPixmap(pixmap.scaled(
                self.avatar_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
        else: # 預設圖片，如果使用者未提供 avatar_path
            self.avatar_label.setStyleSheet("background-color: #DDDDDD; border-radius: 20px;")

        # 2. 建立名稱 QLabel
        self.name_label = QLabel(name)
        font = self.name_label.font()
        font.setBold(True)
        self.name_label.setFont(font)

        # 3. 建立內文 QLabel
        self.content_label = QLabel(content)
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 4. 佈局文字部分 (名稱和內文)
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(5)
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.content_label)

        # 將文字佈局放入一個 QWidget 中，方便管理
        # 這裡 text_widget 不需要 parent，因為它會被加到 main_layout 中
        text_widget = QWidget()
        text_widget.setLayout(text_layout)

        # 5. 建立主佈局 (頭像和文字區塊)
        # main_layout 的 parent 設定為 self 是正確的
        main_layout = QHBoxLayout(self) 
        main_layout.setSpacing(10)
        main_layout.addWidget(self.avatar_label, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(text_widget)


class Message(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 創建滾動區域
        main_layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea() # 僅接收一個 QWidget
        self.scroll_area.setWidgetResizable(True)

        # 創建 message layout
        self.message_list_widget = QWidget()
        self.message_layout = QVBoxLayout(self.message_list_widget)
        self.message_layout.addStretch()

        self.scroll_area.setWidget(self.message_list_widget)

        # 建立下半部 (輸入框和按鈕)
        input_layout = QHBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("在這裡輸入訊息...")
        self.text_input.setMaximumHeight(100) # 限制最大高度
        self.send_button = QPushButton("傳送")
        
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)

        # 7. 【新增】將上下兩部分組合到主佈局中
        main_layout.addWidget(self.scroll_area) # 上半部
        main_layout.addLayout(input_layout)   # 下半部

        # 8. 【新增】連接按鈕的點擊事件到一個新方法
        self.send_button.clicked.connect(self.send_message)

        self.init_add_messages()

    def init_add_messages(self):
        '''
        取得先前的所有訊息，並將他們初始化進 layout
        '''
        for m in MESSAGES:
            self.add_message(m['role'], m['content']) # type: ignore
    
    def add_message(self, role: Literal['user', 'assistant'], content: str):
        '''將訊息加入置 message_layout 當中'''
        new_message = ChatMessageWidget(role, content, None) # 如果有需要的話，在這裡放上 avatar_path 的邏輯
        
        # 將新訊息插入到彈簧（最後一個元件）之前
        self.message_layout.insertWidget(self.message_layout.count() - 1, new_message)
        
        # 新增訊息後，自動滾動到底部
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """ 確保捲動區域總是顯示最新的訊息 """
        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue( # type: ignore
            self.scroll_area.verticalScrollBar().maximum() # type: ignore
        ))

    def send_message(self):
        """ 處理傳送按鈕的點擊事件 """
        user_text = self.text_input.toPlainText().strip()
        if user_text:
            self.add_message('user', user_text)
            self.text_input.clear()
    
            self.ai_response(user_text)

    def ai_response(self, user_text: str): # TODO: 務必修改此處的邏輯，不然 AI 只會回覆你 剛剛說了什麼話而已
        """ 模擬 AI 的回覆 """
        ai_response = f"我收到了您的訊息：'{user_text}'。"
        self.add_message('assistant', ai_response)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    message = Message()
    message.show()
    sys.exit(app.exec())