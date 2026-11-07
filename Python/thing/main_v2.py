import pygame as p

p.init()
p.mixer.init()
p.font.init()

screen = p.display.set_mode((1280, 720))
selection_overlay = p.Surface(screen.get_size(), p.SRCALPHA)
p.display.set_caption("[PLACEHOLDER]")

clock = p.time.Clock()

background = p.image.load("thing/files/wallpaper.png").convert()
background = p.transform.scale(background, (1280, 720))

click_start = p.mixer.Sound("thing/files/click_start.mp3")
click_end = p.mixer.Sound("thing/files/click_end.mp3")
shutdown_sound = p.mixer.Sound("thing/files/shutdown.mp3")

font = p.font.Font("thing/files/Silkscreen.ttf", 18)
time_font = p.font.Font("thing/files/Silkscreen.ttf", 14)

desktop_shortcuts = []
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
    email_icon = p.image.load("thing/files/email_icon.png").convert_alpha()
    email_icon = p.transform.scale(email_icon, (75, 75))
    screen.blit(email_icon, (30, 30))
    email_label = font.render("Email", True, (0, 0, 0))
    email_label_rect = email_label.get_rect(center=(68, 110))
    screen.blit(email_label, email_label_rect)
    img = None
    if unread_emails > 9:
        img = p.image.load("thing/files/notification_9+.png").convert_alpha()
    else:
        img = p.image.load(f"thing/files/notification_{str(unread_emails)}.png").convert_alpha()
    img = p.transform.scale(img, (30, 30))
    screen.blit(img, (85, 35))
    img = p.image.load("thing/files/calendar_icon.png").convert_alpha()
    img = p.transform.scale(img, (75, 75))
    screen.blit(img, (30, 130))
    calendar_label = font.render("Calendar", True, (0, 0, 0))
    calendar_label_rect = calendar_label.get_rect(center=(68, 210))
    screen.blit(calendar_label, calendar_label_rect)

def draw_selections(mouse_before, mouse_after):
    if email_shortcut_selected:
        p.draw.rect(selection_overlay, (0, 128, 255, 128), p.Rect(15, 25, 105, 105))
        p.draw.rect(selection_overlay, (0, 0, 255), p.Rect(15, 25, 105, 105), width=2)
    if calendar_shortcut_selected:
        p.draw.rect(selection_overlay, (0, 128, 255, 128), p.Rect(15, 125, 105, 105))
        p.draw.rect(selection_overlay, (0, 0, 255), p.Rect(15, 125, 105, 105), width=2)
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

def draw_email_window():
    frame_rect = p.Rect(0, 0, 1000, 500)
    frame_rect.center = email_window_pos
    p.draw.rect(screen, (212, 207, 201), frame_rect)

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
                    pressing.append(("start", p.Rect(20, 670, 125, 40)))
                if p.Rect(40, 570, 40, 40).collidepoint(event.pos):
                    pressing.append(("shutdown", p.Rect(40, 570, 40, 40)))
                if p.Rect(30, 30, 75, 75).collidepoint(event.pos):
                    pressing.append(("email_shortcut", p.Rect(30, 30, 75, 75)))
                if p.Rect(30, 130, 75, 75).collidepoint(event.pos):
                    pressing.append(("calendar_shortcut", p.Rect(30, 130, 75, 75)))
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
                    if p.Rect(30, 30, 75, 75).colliderect(p.Rect(min(mouse_before[0], mouse_after[0]), min(mouse_before[1], mouse_after[1]), abs(mouse_after[0] - mouse_before[0]), abs(mouse_after[1] - mouse_before[1]))):
                        email_shortcut_selected = True
                    if p.Rect(30, 130, 75, 75).colliderect(p.Rect(min(mouse_before[0], mouse_after[0]), min(mouse_before[1], mouse_after[1]), abs(mouse_after[0] - mouse_before[0]), abs(mouse_after[1] - mouse_before[1]))):
                        calendar_shortcut_selected = True
                selection_box = False
                for i, (name, rect) in enumerate(pressing):
                    if name == "start" and rect.collidepoint(event.pos):
                        start_menu_open = not start_menu_open
                    if name == "shutdown" and rect.collidepoint(event.pos):
                        running = False
                    if name == "email_shortcut" and rect.collidepoint(event.pos):
                        if elapsed_time - email_timer < 0.5:
                            email_activated = True
                            email_timer = -10
                            email_shortcut_selected = False
                        else:
                            email_timer = elapsed_time
                            email_shortcut_selected = not email_shortcut_selected
                        calendar_shortcut_selected = False
                    if name == "calendar_shortcut" and rect.collidepoint(event.pos):
                        if elapsed_time - calendar_timer < 0.5:
                            calendar_activated = True
                            calendar_timer = -10
                            calendar_shortcut_selected = False
                        else:
                            calendar_timer = elapsed_time
                            calendar_shortcut_selected = not calendar_shortcut_selected
                        email_shortcut_selected = False
                pressing.clear()
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
    if start_menu_open:
        draw_start_menu()
    if email_activated:
        draw_email_window()
    p.display.flip()
    time_delta = clock.tick(60)/1000
    selection_overlay.fill((0, 0, 0, 0))

shutdown_sound.play()
screen.fill((0, 0, 0))
p.display.flip()
while shutdown_sound.get_num_channels() > 0:
    p.time.delay(1)