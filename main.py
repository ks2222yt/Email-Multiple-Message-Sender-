import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dearpygui.dearpygui as gui
import time
import threading
import mouse

name = 'NOT $P4MM3R PLZ GITHUB DO NOT DELETE'

def send_email(sender, receiver, subject, body, password):
    msg = MIMEMultipart()
    msg["From"], msg["To"], msg["Subject"] = sender, receiver, subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("sent!")
    except Exception as e:
        print(e)

def main():
    while True:
        time.sleep(0.1)
        if gui.get_value('active'):
            send_email(
                sender=gui.get_value('sender'),
                receiver=gui.get_value('receiver'),
                subject=gui.get_value('message'),
                body=gui.get_value('body'),
                password=gui.get_value('smtp_pass')
            )

def threads():
    global th
    th = threading.Thread(target=main,daemon=True)
    th.start()
    start_gui()


def start_gui():
    gui_height = 400
    gui_width = 600
    theme_color = (0,255,255,255)
    
    gui.create_context()
    gui.create_viewport(title=f'niga', width=gui_width, height=gui_height, decorated=False)
    gui.setup_dearpygui()
    gui.set_viewport_resizable(False)

    with gui.theme() as all_theme:
        with gui.theme_component(gui.mvAll):
            gui.add_theme_color(gui.mvThemeCol_WindowBg, (5, 5, 5, 255))

            gui.add_theme_color(gui.mvThemeCol_Button, (25, 25, 25, 255))
            gui.add_theme_color(gui.mvThemeCol_ButtonHovered, (50, 50, 50, 255))
            gui.add_theme_color(gui.mvThemeCol_ButtonActive, (60, 60, 60, 255))

            gui.add_theme_color(gui.mvThemeCol_Text, theme_color)

            gui.add_theme_color(gui.mvThemeCol_Border, theme_color)
            gui.add_theme_color(gui.mvThemeCol_BorderShadow, theme_color)

            gui.add_theme_color(gui.mvThemeCol_CheckMark, theme_color)

            gui.add_theme_color(gui.mvThemeCol_FrameBg, (25, 25, 25, 255))
            gui.add_theme_color(gui.mvThemeCol_FrameBgHovered, (45, 45, 45, 255))
            gui.add_theme_color(gui.mvThemeCol_FrameBgActive, (65, 65, 65, 255))

            gui.add_theme_color(gui.mvThemeCol_Separator, theme_color)
            
            gui.add_theme_style(gui.mvStyleVar_ChildRounding,0)
            gui.add_theme_style(gui.mvStyleVar_WindowBorderSize,0)
            gui.add_theme_style(gui.mvStyleVar_ChildBorderSize,1)
            gui.add_theme_style(gui.mvStyleVar_FrameRounding,0)
            gui.add_theme_style(gui.mvStyleVar_GrabRounding,2)

    class gui_funcs:
        def move_gui():
            while True:
                mouse_pos = mouse.get_position()
                gui.set_viewport_pos(pos=(mouse_pos[0]-gui_width/2,mouse_pos[1]))
                if mouse.is_pressed('left'):break

        def minimize_viewport():
            gui.minimize_viewport()

    input_width = 400
    window_width = gui_width
    x_center = (window_width - input_width) // 2
    pos_y = 100

    gui_width+=74

    with gui.window(label='', width=gui_width, height=gui_height, no_title_bar=True, no_resize=True, no_move=True, show=True, tag='mainwindow', no_scroll_with_mouse=True, no_scrollbar=True):
        with gui.group(pos=(0,0)):
            gui.add_separator(pos=(0,0))
            gui.add_button(label=f'{name}', callback=gui_funcs.move_gui,   width=gui_width-180, height=20, pos=(0,  1),tag='name_button')
            gui.add_button(label="-", callback=gui_funcs.minimize_viewport,width=54, height=20, pos=(gui_width-181, 1),tag='minim_button')
            gui.add_button(label="X", callback=lambda:gui.destroy_context(),   width=54, height=20, pos=(gui_width-128, 1),tag='close_button')

        with gui.group(pos=(x_center,pos_y)):
            gui.add_input_text(tag='receiver', hint='Target Mail',          width = input_width)
            gui.add_input_text(tag='sender', hint='Your Mail',              width = input_width)
            gui.add_input_text(tag='smtp_pass', hint='Gmail SMTP Password', width = input_width, password=True)
            gui.add_input_text(tag='message', hint='Subject',               width = input_width)
            gui.add_input_text(tag='body', hint='Message',                  width = input_width)
            gui.add_spacer(height=10)
            gui.add_checkbox(label='active', tag='active')



    gui.bind_theme(all_theme)

    gui.show_viewport()
    gui.start_dearpygui()
    gui.destroy_context()

if __name__ == '__main__':
    threads()
