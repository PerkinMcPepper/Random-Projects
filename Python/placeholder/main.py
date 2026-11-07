import pygame as p
import pygame_gui as gui

p.init()
p.mixer.init()

screen = p.display.set_mode((1280, 720))
selection_overlay = p.Surface(screen.get_size(), p.SRCALPHA)
manager = gui.UIManager((1280, 720), "thing/files/theme.json")
desktop_label_manager = gui.UIManager((1280, 720), "thing/files/theme.json")
p.display.set_caption("[PLACEHOLDER]")

clock = p.time.Clock()

background = p.image.load("thing/files/wallpaper.png").convert()
background = p.transform.scale(background, (1280, 720))

click_start = p.mixer.Sound("thing/files/click_start.mp3")
click_end = p.mixer.Sound("thing/files/click_end.mp3")

apps = []
desktop_shortcuts = []
time = ""
date = ""

start_button = gui.elements.UIButton(p.Rect(20, 670, 125, 40), "     Start", manager=manager)
start_button_pressed = False
start_menu_open = False
shutdown_button = gui.elements.UIButton(p.Rect(40, 570, 40, 40), "",  manager=manager)
shutdown_label = gui.elements.UILabel(p.Rect(90, 570, 100, 40), "", manager=manager)

email_shortcut = gui.elements.UIButton(p.Rect(20, 20, 75, 75), "", manager=manager, allow_double_clicks=True)
email_shortcut_label = gui.elements.UILabel(p.Rect(20, 85, 75, 25), "Email", manager=desktop_label_manager)
unread_emails = 0
email_shortcut_selected = False

calendar_shortcut = gui.elements.UIButton(p.Rect(20, 120, 75, 75), "", manager=manager, allow_double_clicks=True)
calendar_shortcut_label = gui.elements.UILabel(p.Rect(20, 190, 75, 25), "Calendar", manager=desktop_label_manager)
calendar_schedule = []
calendar_shortcut_selected = False

time_label = gui.elements.UILabel(p.Rect(1165, 675, 100, 15), time, manager=manager, object_id="#time_label")
date_label = gui.elements.UILabel(p.Rect(1165, 690, 100, 15), date, manager=manager, object_id="#time_label")

def draw_bevel(rect, colour, variation, width):
    p.draw.polygon(screen, tuple(min(255, (c + variation if width > 0 else c - variation)) for c in colour), [rect.topleft, (rect.right-1, rect.top), (rect.right - abs(width) - 1, rect.top + abs(width)), (rect.left + abs(width), rect.top + abs(width))])
    p.draw.polygon(screen, tuple(min(255,(c + variation if width > 0 else c - variation)) for c in colour), [rect.topleft, (rect.left, rect.bottom-1), (rect.left + abs(width), rect.bottom - abs(width) - 1), (rect.left + abs(width), rect.top + abs(width))])
    p.draw.polygon(screen, tuple(max(0, (c - variation if width > 0 else c + variation)) for c in colour), [(rect.right-1, rect.top), (rect.right-1, rect.bottom - 1), (rect.right - abs(width) - 1, rect.bottom - abs(width) - 1), (rect.right - abs(width) - 1, rect.top + abs(width))])
    p.draw.polygon(screen, tuple(max(0, (c - variation if width > 0 else c + variation)) for c in colour), [(rect.left, rect.bottom - 1), (rect.right-1, rect.bottom - 1), (rect.right - abs(width) - 1, rect.bottom - abs(width) - 1), (rect.left + abs(width), rect.bottom - abs(width) - 1)])

def draw_background():
    screen.blit(background, (0, 0))

def draw_desktop_selections():
    if email_shortcut_selected:
        p.draw.rect(selection_overlay, (0, 128, 255, 128), p.Rect(10, 20, 95, 95))
        p.draw.rect(selection_overlay, (0, 0, 255), p.Rect(10, 20, 95, 95), width=2) 
    if calendar_shortcut_selected:
        p.draw.rect(selection_overlay, (0, 128, 255, 128), p.Rect(10, 120, 95, 95))
        p.draw.rect(selection_overlay, (0, 0, 255), p.Rect(10, 120, 95, 95), width=2) 

def draw_desktop_shortcuts():
    email_icon = p.image.load("thing/files/email_icon.png").convert_alpha()
    email_icon = p.transform.scale(email_icon, (75, 75))
    screen.blit(email_icon, (20, 20))
    img = None
    if unread_emails > 9:
        img = p.image.load("thing/files/notification_9+.png").convert_alpha()
    else:
        img = p.image.load(f"thing/files/notification_{str(unread_emails)}.png").convert_alpha()
    img = p.transform.scale(img, (30, 30))
    screen.blit(img, (75, 25))
    img = p.image.load("thing/files/calendar_icon.png").convert_alpha()
    img = p.transform.scale(img, (75, 75))
    screen.blit(img, (20, 120))

def draw_taskbar():
    taskbar_rect = p.Rect(0, 660, 1280, 60)
    p.draw.rect(screen, (212, 207, 201), taskbar_rect)
    draw_bevel(taskbar_rect, (212, 207, 201), 20, 5)

    both_rect = p.Rect(1165, 670, 100, 40)
    draw_bevel(both_rect, (212, 207, 201), 20, -5)

def draw_taskbar_buttons():
    start_rect = p.Rect(20, 670, 125, 40)
    draw_bevel(start_rect, (212, 207, 201), 20, (2 if start_button_pressed else 5))
    start_imgwidth = start_rect.height - 10
    img = p.image.load("thing/files/start_icon.png").convert_alpha()
    img = p.transform.scale(img, (start_imgwidth, start_imgwidth))
    screen.blit(img, (start_rect.left + 15, start_rect.top + 5))

def draw_start_menu():
    start_menu_rect = p.Rect(20, 330, 300, 300)
    p.draw.rect(screen, (212, 207, 201), start_menu_rect)
    img = p.image.load("thing/files/shutdown.png").convert_alpha()
    img = p.transform.scale(img, (40, 40))
    screen.blit(img, (40, 570))

def set_time_date(elapsed):
    e_m = elapsed * 0.4
    m = int(e_m % 60)
    h = int(e_m // 60) + 9
    global time, date, time_label, date_label
    time_label.set_text(f"{h}:{str(m) if m >= 10 else f'0{m}'}")
    date_label.set_text("01/12/2024")

elapsed_time = 0
last_email_press = 0
running = True
pressed = False
dragging = False
mouse_before = (0, 0)
mouse_after = (0, 0)
while running:
    time_delta = clock.tick(60)/1000
    elapsed_time += time_delta
    set_time_date(elapsed_time)
    manager.update(time_delta)
    for event in p.event.get():
        manager.process_events(event)
        if event.type == p.QUIT:
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button != 2:
                click_start.play()
            if event.button == 1:
                pressed = True
                mouse_before = p.mouse.get_pos()
                mouse_after = p.mouse.get_pos()
        if event.type == p.MOUSEBUTTONUP:
            if event.button != 2:
                click_end.play()
            if event.button == 1:
                start_button_pressed = False
                pressed = False
                if not email_shortcut.rect.collidepoint(p.mouse.get_pos()) and not calendar_shortcut.rect.collidepoint(p.mouse.get_pos()):
                    email_shortcut_selected = False
                    print("Email False 1")
                    calendar_shortcut_selected = False
                    print("Calendar False 1")
                if dragging:
                    dragging = False
                    if min(mouse_before[0], mouse_after[0]) <= p.Rect(10, 20, 95, 95).centerx <= max(mouse_before[0], mouse_after[0]) and min(mouse_before[1], mouse_after[1]) <= p.Rect(10, 20, 95, 95).centery <= max(mouse_before[1], mouse_after[1]):
                        email_shortcut_selected = True
                        print("Email True 1")
                    if min(mouse_before[0], mouse_after[0]) <= p.Rect(10, 120, 95, 95).centerx <= max(mouse_before[0], mouse_after[0]) and min(mouse_before[1], mouse_after[1]) <= p.Rect(10, 120, 95, 95).centery <= max(mouse_before[1], mouse_after[1]):
                        calendar_shortcut_selected = True
                        print("Calendar True 1")
        if event.type == p.MOUSEMOTION:
            if pressed:
                dragging = True
                mouse_after = p.mouse.get_pos()
        if event.type == gui.UI_BUTTON_START_PRESS:
            if event.ui_element == start_button:
                start_button_pressed = True
        if event.type == gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                start_menu_open = not start_menu_open
            if event.ui_element == email_shortcut:
                email_shortcut_selected = True
                print("Email True 2")
                print("Calendar False 2")
                calendar_shortcut_selected = False
            if event.ui_element == calendar_shortcut:
                calendar_shortcut_selected = True
                email_shortcut_selected = False
                print("Email False 2")
                print("Calendar True 2")
            if event.ui_element == shutdown_button:
                running = False
        if event.type == gui.UI_BUTTON_DOUBLE_CLICKED:
            if event.ui_element == email_shortcut:
                email_shortcut_selected = False
                calendar_shortcut_selected = False
                print("Email False 3")
                print("Calendar False 3")
            if event.ui_element == calendar_shortcut:
                calendar_shortcut_selected = False
                email_shortcut_selected = False
                print("Email False 4")
                print("Calendar False 4")

    selection_overlay.fill((0, 0, 0, 0))
    draw_background()
    draw_desktop_shortcuts()
    desktop_label_manager.update(time_delta)
    desktop_label_manager.draw_ui(screen)
    if dragging:
        select_rect = p.Rect(min(mouse_before[0], mouse_after[0]), min(mouse_before[1], mouse_after[1]), abs(mouse_after[0] - mouse_before[0]), abs(mouse_after[1] - mouse_before[1]))
        p.draw.rect(selection_overlay, (0, 128, 255, 128), select_rect)
    draw_desktop_selections()
    screen.blit(selection_overlay, (0, 0))
    draw_taskbar()
    draw_taskbar_buttons()
    if start_menu_open:
        draw_start_menu()
    shutdown_label.set_text("Shutdown" if start_menu_open else "")
    manager.draw_ui(screen)
    p.display.flip()
    selected = False