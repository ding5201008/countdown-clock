from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.utils import platform

# 设置应用支持屏幕旋转
Config.set('graphics', 'orientation', 'portrait')
Config.set('graphics', 'resizable', '1')

# 设置全屏
Window.fullscreen = 'auto'


class CountdownClockApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.remaining_seconds = 0
        self.is_running = False
        self.original_title = "全屏倒计时时钟"
        
    def build(self):
        # 设置应用标题
        self.title = self.original_title
        
        # 创建主布局 - 垂直排列
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 创建时间显示标签
        self.time_display = Label(
            text="00:00:00",
            font_size='80sp',
            size_hint=(1, 0.4)
        )
        main_layout.add_widget(self.time_display)
        
        # 创建倒计时显示标签
        self.countdown_display = Label(
            text="倒计时: 00:00:00",
            font_size='40sp',
            size_hint=(1, 0.2)
        )
        main_layout.add_widget(self.countdown_display)
        
        # 创建输入区域
        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        # 小时输入
        self.hours_input = TextInput(
            text='0',
            multiline=False,
            input_filter='int',
            size_hint=(0.3, 1),
            font_size='24sp'
        )
        input_layout.add_widget(Label(text='时', size_hint=(0.2, 1)))
        input_layout.add_widget(self.hours_input)
        
        # 分钟输入
        self.minutes_input = TextInput(
            text='0',
            multiline=False,
            input_filter='int',
            size_hint=(0.3, 1),
            font_size='24sp'
        )
        input_layout.add_widget(Label(text='分', size_hint=(0.2, 1)))
        input_layout.add_widget(self.minutes_input)
        
        # 秒输入
        self.seconds_input = TextInput(
            text='0',
            multiline=False,
            input_filter='int',
            size_hint=(0.3, 1),
            font_size='24sp'
        )
        input_layout.add_widget(Label(text='秒', size_hint=(0.2, 1)))
        input_layout.add_widget(self.seconds_input)
        
        main_layout.add_widget(input_layout)
        
        # 创建按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        self.start_button = Button(
            text='开始倒计时',
            on_press=self.start_countdown,
            background_color=(0, 0.7, 0, 1)  # 绿色
        )
        button_layout.add_widget(self.start_button)
        
        self.pause_button = Button(
            text='暂停',
            on_press=self.pause_countdown,
            background_color=(0.9, 0.6, 0, 1),  # 橙色
            disabled=True
        )
        button_layout.add_widget(self.pause_button)
        
        self.reset_button = Button(
            text='重置',
            on_press=self.reset_countdown,
            background_color=(0.8, 0, 0, 1)  # 红色
        )
        button_layout.add_widget(self.reset_button)
        
        main_layout.add_widget(button_layout)
        
        # 创建屏幕方向切换按钮
        orientation_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        self.portrait_button = ToggleButton(
            text='竖屏',
            group='orientation',
            state='down',
            on_press=self.set_portrait
        )
        orientation_layout.add_widget(self.portrait_button)
        
        self.landscape_button = ToggleButton(
            text='横屏',
            group='orientation',
            on_press=self.set_landscape
        )
        orientation_layout.add_widget(self.landscape_button)
        
        main_layout.add_widget(orientation_layout)
        
        # 创建全屏切换按钮
        fullscreen_button = Button(
            text='切换全屏',
            on_press=self.toggle_fullscreen,
            size_hint=(1, 0.1),
            background_color=(0, 0.5, 0.8, 1)  # 蓝色
        )
        main_layout.add_widget(fullscreen_button)
        
        # 设置定时器更新时钟
        Clock.schedule_interval(self.update_clock, 1)
        
        return main_layout
    
    def update_clock(self, dt):
        # 更新当前时间显示
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_display.text = current_time
        
        # 更新倒计时
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_countdown_display()
            
            # 倒计时结束提示
            if self.remaining_seconds == 0:
                self.countdown_display.text = "时间到!"
                self.is_running = False
                self.start_button.disabled = False
                self.pause_button.disabled = True
                # 这里可以添加声音或振动提示
    
    def update_countdown_display(self):
        # 格式化显示倒计时时间
        hours = self.remaining_seconds // 3600
        minutes = (self.remaining_seconds % 3600) // 60
        seconds = self.remaining_seconds % 60
        self.countdown_display.text = f"倒计时: {hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def start_countdown(self, instance):
        try:
            # 从输入框获取时间
            hours = int(self.hours_input.text) if self.hours_input.text else 0
            minutes = int(self.minutes_input.text) if self.minutes_input.text else 0
            seconds = int(self.seconds_input.text) if self.seconds_input.text else 0
            
            # 计算总秒数
            total_seconds = hours * 3600 + minutes * 60 + seconds
            
            if total_seconds > 0:
                self.remaining_seconds = total_seconds
                self.is_running = True
                self.update_countdown_display()
                self.start_button.disabled = True
                self.pause_button.disabled = False
                self.title = f"{self.original_title} - 倒计时中"
            else:
                self.countdown_display.text = "请输入有效时间"
                
        except ValueError:
            self.countdown_display.text = "请输入数字"
    
    def pause_countdown(self, instance):
        self.is_running = not self.is_running
        if self.is_running:
            self.pause_button.text = "暂停"
            self.title = f"{self.original_title} - 倒计时中"
        else:
            self.pause_button.text = "继续"
            self.title = f"{self.original_title} - 已暂停"
    
    def reset_countdown(self, instance):
        self.is_running = False
        self.remaining_seconds = 0
        self.countdown_display.text = "倒计时: 00:00:00"
        self.start_button.disabled = False
        self.pause_button.disabled = True
        self.pause_button.text = "暂停"
        self.title = self.original_title
    
    def set_portrait(self, instance):
        # 设置竖屏
        from kivy.config import Config
        Config.set('graphics', 'orientation', 'portrait')
    
    def set_landscape(self, instance):
        # 设置横屏
        from kivy.config import Config
        Config.set('graphics', 'orientation', 'landscape')
    
    def toggle_fullscreen(self, instance):
        # 切换全屏状态
        Window.fullscreen = 'auto' if Window.fullscreen == False else False


if __name__ == '__main__':
    CountdownClockApp().run()