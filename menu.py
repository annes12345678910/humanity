import ultimateraylib as rl
import asset, connect
cam = rl.make_camera(
    rl.Vector3(10, 2, 10),
    rl.Vector3(0,0,0),
    rl.Vector3(0, 1, 0),
    60,
    rl.CAMERA_PERSPECTIVE
)

bg = asset.load_model("assets/humanscene.glb")
logo = asset.load_texture("assets/logo.png")
music = asset.load_music("assets/howitsdone.mp3")
rl.play_music_stream(music)
winsize: rl.Vector2
iptojoin = ""
ismenu = True
shouldquit = False
def draw():
    global cam, winsize, iptojoin, ismenu, shouldquit
    if not ismenu:
        return
    winsize = rl.Vector2(rl.get_screen_width(), rl.get_screen_height())
    cam = rl.update_camera(cam, rl.CAMERA_ORBITAL)
    rl.update_music_stream(music)
    rl.clear_background(rl.SKYBLUE)
    rl.begin_mode_3d(cam)
    rl.draw_model(bg, rl.Vector3(0,0,0), 1, rl.WHITE)
    rl.end_mode_3d()
    rl.draw_texture(logo, int(winsize.x / 2) - 150, int(winsize.y / 2) - 300, rl.WHITE)
    if rl.gui_button(rl.Rectangle(int(winsize.x / 2) - 150, int(winsize.y / 2) + 30, 300, 100), "Play"):
        print(f"Trying to connect to {iptojoin}")
        try:
            connect.connectoserver(iptojoin)
        except:
            print("Failed to connect. Starting singleplayer world")
            shouldquit = True
            import singleplayer
            return
        
        rl.stop_music_stream(music)
    if rl.gui_button(rl.Rectangle(int(winsize.x / 2) - 150, int(winsize.y / 2) + 200, 300, 100), "Quit"):
        shouldquit = True
    if rl.is_key_down(rl.KEY_LEFT_SUPER) and rl.is_key_down(rl.KEY_V):
        iptojoin = rl.get_clipboard_text().decode()
    k, iptojoin = rl.gui_text_box(rl.Rectangle(int(winsize.x / 2) - 350, int(winsize.y / 2), 180, 50), iptojoin, 1024, True)
