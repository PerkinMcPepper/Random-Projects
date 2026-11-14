import pygame as p

p.init()
p.mixer.init()
p.font.init()

click_start = p.mixer.Sound("thing/files/click_start.mp3")
click_end = p.mixer.Sound("thing/files/click_end.mp3")
startup_sound = p.mixer.Sound("thing/files/startup.mp3")
shutdown_sound = p.mixer.Sound("thing/files/shutdown.mp3")

screen = p.display.set_mode((1280, 720))
selection_overlay = p.Surface(screen.get_size(), p.SRCALPHA)
p.display.set_caption("[PLACEHOLDER]")

clock = p.time.Clock()

background = p.image.load("thing/files/wallpaper.png").convert()
background = p.transform.scale(background, (1280, 720))

font = p.font.Font("thing/files/Silkscreen.ttf", 18)
time_font = p.font.Font("thing/files/Silkscreen.ttf", 14)

id = -1

desktop_shortcuts = [{
    "name": "Email",
    "image": "thing/files/email_icon.png",
    "rect": p.Rect(30, 30, 75, 75),
    "img-rect": p.Rect(30, 30, 75, 75),
    "func": lambda: exec("windows.append((\"email\", p.Rect(290, 110, 700, 500), id + 1))\nid += 1", globals()),
    "select-rect": p.Rect(15, 25, 105, 105),
    "text-center": (68, 110),
    "selected": False,
    "timer": -10
    },
    {
    "name": "Calendar",
    "image": "thing/files/calendar_icon.png",
    "rect": p.Rect(30, 130, 75, 75),
    "img-rect": p.Rect(30, 130, 75, 75),
    "func": lambda: exec("windows.append((\"calendar\", p.Rect(290, 110, 700, 500), id + 1))\nid += 1", globals()),
    "select-rect": p.Rect(15, 125, 105, 105),
    "text-center": (68, 210),
    "selected": False,
    "timer": -10
    }]
#note to self
#dict structure is name=, image=, rect=, img-rect=, func=, select-rect=, text-center=, selected=, timer=, active=
windows = []
time = ""
date = ""
unread_emails = 0

def draw_bevel(rect, colour, variation, width):
    p.draw.polygon(screen, tuple(min(255, (c + variation if width > 0 else c - variation)) for c in colour), [rect.topleft, (rect.right-1, rect.top), (rect.right - abs(width) - 1, rect.top + abs(width)), (rect.left + abs(width), rect.top + abs(width))])
    p.draw.polygon(screen, tuple(min(255,(c + variation if width > 0 else c - variation)) for c in colour), [rect.topleft, (rect.left, rect.bottom-1), (rect.left + abs(width), rect.bottom - abs(width) - 1), (rect.left + abs(width), rect.top + abs(width))])
    p.draw.polygon(screen, tuple(max(0, (c - variation if width > 0 else c + variation)) for c in colour), [(rect.right-1, rect.top), (rect.right-1, rect.bottom - 1), (rect.right - abs(width) - 1, rect.bottom - abs(width) - 1), (rect.right - abs(width) - 1, rect.top + abs(width))])
    p.draw.polygon(screen, tuple(max(0, (c - variation if width > 0 else c + variation)) for c in colour), [(rect.left, rect.bottom - 1), (rect.right-1, rect.bottom - 1), (rect.right - abs(width) - 1, rect.bottom - abs(width) - 1), (rect.left + abs(width), rect.bottom - abs(width) - 1)])

def draw_background():
    screen.blit(background, (0, 0))

def draw_desktop_shortcuts():
    for shortcut in desktop_shortcuts:
        icon = p.image.load(shortcut["image"]).convert_alpha()
        icon = p.transform.scale(icon, shortcut["img-rect"].size)
        screen.blit(icon, shortcut["img-rect"].topleft)
        label = font.render(shortcut["name"], True, (0, 0, 0))
        label_rect = label.get_rect(center=(shortcut["text-center"]))
        screen.blit(label, label_rect)

        if shortcut["name"] == "Email":
            img = None
            if unread_emails > 9:
                img = p.image.load("thing/files/notification_9+.png").convert_alpha()
            else:
                img = p.image.load(f"thing/files/notification_{str(unread_emails)}.png").convert_alpha()
            img = p.transform.scale(img, (30, 30))
            temp_pos = shortcut["img-rect"].topleft
            screen.blit(img, (temp_pos[0]+55, temp_pos[1]+5))

def draw_selections(mouse_before, mouse_after):
    for shortcut in desktop_shortcuts:
        if shortcut["selected"]:
            p.draw.rect(selection_overlay, (0, 128, 255, 128), shortcut["select-rect"])
            p.draw.rect(selection_overlay, (0, 0, 255), shortcut["select-rect"], width=2)
    
    if mouse_before != mouse_after:
        selection_rect = p.Rect(min(mouse_before[0], mouse_after[0]), min(mouse_before[1], mouse_after[1]), abs(mouse_after[0] - mouse_before[0]), abs(mouse_after[1] - mouse_before[1]))
        p.draw.rect(selection_overlay, (0, 128, 255, 128), selection_rect)
        p.draw.rect(selection_overlay, (0, 0, 255), selection_rect, width=2)
    screen.blit(selection_overlay, (0, 0))

def draw_taskbar():
    taskbar_rect = p.Rect(0, 660, 1280, 60)
    p.draw.rect(screen, (212, 207, 201), taskbar_rect)
    draw_bevel(taskbar_rect, (212, 207, 201), 20, 5)

    both_rect = p.Rect(1155, 670, 120, 40)
    draw_bevel(both_rect, (212, 207, 201), 20, -5)

def draw_time_date(elapsed):
    e_m = elapsed * 0.4
    m = int(e_m % 60)
    h = int(e_m // 60) + 9
    time = time_font.render(f"{h}:{str(m) if m >= 10 else f'0{m}'}", True, (0, 0, 0))
    date = time_font.render("01/12/2024", True, (0, 0, 0))
    time_rect = time.get_rect(center=(1215, 680))
    date_rect = date.get_rect(center=(1215, 695))
    screen.blit(time, time_rect)
    screen.blit(date, date_rect)

def draw_taskbar_buttons(pressed):
    start_rect = p.Rect(20, 670, 125, 40)
    draw_bevel(start_rect, (212, 207, 201), 20, (2 if pressed else 5))
    start_imgwidth = start_rect.height - 10
    img = p.image.load("thing/files/start_icon.png").convert_alpha()
    img = p.transform.scale(img, (start_imgwidth, start_imgwidth))
    screen.blit(img, (start_rect.left + 15, start_rect.top + 5))
    start_text = font.render("Start", True, (0, 0, 0))
    start_text_rect = start_text.get_rect(center=(start_rect.centerx+20, start_rect.centery))
    screen.blit(start_text, start_text_rect)

def draw_start_menu():
    start_menu_rect = p.Rect(20, 340, 300, 300)
    p.draw.rect(screen, (212, 207, 201), start_menu_rect)
    img = p.image.load("thing/files/shutdown.png").convert_alpha()
    img = p.transform.scale(img, (40, 40))
    screen.blit(img, (40, 570))
    shutdown_text = font.render("Shutdown", True, (0, 0, 0))
    shutdown_text_rect = shutdown_text.get_rect(center=(150, 590))
    screen.blit(shutdown_text, shutdown_text_rect)

def draw_windows():
    global windows
    for window in windows:
        if window[0] == "email":
            p.draw.rect(screen, (212, 207, 201), window[1])
            draw_bevel(window[1], (212, 207, 201), 30, 2)
            top_bar = p.Rect(window[1].x+3, window[1].y+3, window[1].width-6, 40)
            p.draw.rect(screen, (0, 0, 255), top_bar)
            icon = p.image.load("thing/files/email_icon.png")
            icon = p.transform.scale(icon, (30, 30))
            screen.blit(icon, p.Rect(top_bar.x+5, top_bar.y+5, 30, 30))
            text = font.render("Email", True, (255, 255, 255))
            text_rect = text.get_rect(centery = window[1].y+22, x = window[1].x + 50)
            screen.blit(text, text_rect)
            close = p.Rect(top_bar.right - 31, top_bar.centery-10, 20, 20)
            p.draw.rect(screen, (212, 207, 201), close)
            minimise_icon = p.image.load("thing/files/close.png")
            minimise_icon = p.transform.scale(minimise_icon, (20, 20))
            screen.blit(minimise_icon, (close.x, close.y))
            draw_bevel(close, (212, 207, 201), 20, 2)

running = True
time_delta = 0
elapsed_time = 0
pressing = []
start_menu_open = False
selection_box = False
mouse_before = (0, 0)
mouse_after = (0, 0)
email_shortcut_selected = False
email_timer = -10
email_activated = False
email_window_pos = (640, 360)
calendar_shortcut_selected = False
calendar_timer = -10
calendar_activated = False
calendar_window_pos = (640, 360)

do_startup = False

if do_startup:
    screen.fill((0, 0, 0))
    startup_sound.play()
    while startup_sound.get_num_channels() > 0:
        p.time.delay(1)

while running:
    elapsed_time += time_delta
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if event.type == p.MOUSEBUTTONDOWN:
            if event.button != 2:
                click_start.play()
            if event.button == 1:
                if p.Rect(20, 670, 125, 40).collidepoint(event.pos):
                    pressing.append(("start", p.Rect(20, 670, 125, 40), False))
                if p.Rect(40, 570, 40, 40).collidepoint(event.pos):
                    pressing.append(("shutdown", p.Rect(40, 570, 40, 40), False))
                for shortcut in desktop_shortcuts:
                    if shortcut["rect"].collidepoint(event.pos):
                        pressing.append((shortcut["name"], shortcut["rect"], shortcut))
            if len(pressing) == 0:
                selection_box = True
                mouse_before = p.mouse.get_pos()
                mouse_after = p.mouse.get_pos()
                email_shortcut_selected = False
                calendar_shortcut_selected = False
        if event.type == p.MOUSEMOTION:
            if selection_box:
                mouse_after = p.mouse.get_pos()
        if event.type == p.MOUSEBUTTONUP:
            if event.button != 2:
                click_end.play()
            if event.button == 1:
                if selection_box:
                    for shortcut in desktop_shortcuts:
                        if p.Rect(min(mouse_before[0], mouse_after[0]), min(mouse_before[1], mouse_after[1]), abs(mouse_after[0] - mouse_before[0]), abs(mouse_after[1] - mouse_before[1])).collidepoint(shortcut["rect"].center):
                            shortcut["selected"] = True
                        else:
                            shortcut["selected"] = False
                selected = ""
                for i, (name, rect, item) in enumerate(pressing):
                    if not item:
                        if name == "start" and rect.collidepoint(event.pos):
                            start_menu_open = not start_menu_open
                        if name == "shutdown" and rect.collidepoint(event.pos):
                            if start_menu_open:
                                running = False
                    elif item and rect.collidepoint(event.pos):
                        if elapsed_time - item["timer"] < 0.5:
                            item["timer"] = -10
                            item["selected"] = False
                            if item["func"]:
                                item["func"]()
                            print(windows)
                        else:
                            selected = item["name"]
                            print(f"Selected: {selected}")
                            item["timer"] = elapsed_time
                if selected != "":
                    for shortcut in desktop_shortcuts[:]:
                        shortcut["selected"] = (shortcut["name"] == selected)
                elif not selection_box:
                    for shortcut in desktop_shortcuts[:]:
                        shortcut["selected"] = False
                pressing.clear()
                selection_box = False
    pressing = [x for x in pressing if x[1].collidepoint(p.mouse.get_pos())]
    if not selection_box:
        mouse_before = p.mouse.get_pos()
        mouse_after = p.mouse.get_pos()
    draw_background()
    draw_desktop_shortcuts()
    draw_selections(mouse_before, mouse_after)
    draw_taskbar()
    draw_time_date(elapsed_time)
    draw_taskbar_buttons(any(x[0] == "start" for x in pressing))
    draw_windows()
    if start_menu_open:
        draw_start_menu()
    p.display.flip()
    time_delta = clock.tick(60)/1000
    selection_overlay.fill((0, 0, 0, 0))

shutdown_sound.play()
screen.fill((0, 0, 0))
p.display.flip()
while shutdown_sound.get_num_channels() > 0:
    p.time.delay(1)