import math
import ultimateraylib as rl
import ultimateraylib.light as rlight
import asset, config
import random
import connect

cam = rl.make_camera(
    rl.Vector3(10, 2, 10),
    rl.Vector3(0,0,0),
    rl.Vector3(0, 1, 0),
    60,
    rl.CAMERA_PERSPECTIVE
)

bg = asset.load_model("assets/humanscene.glb")
logo = asset.load_texture("assets/logo.png")
music = asset.load_music("assets/aiso.mp3")
rl.play_music_stream(music)
winsize: rl.Vector2
iptojoin = ""
ismenu = True
shouldquit = False
single = False
frame = 0

shader = asset.load_shader("assets/lighting.vs", "assets/lighting.fs")

shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")

ambientLoc = rl.get_shader_location(shader, "ambient")
rl.set_shader_value(shader, ambientLoc, [0.1, 0.1, 0.1, 1], rl.SHADER_UNIFORM_VEC4)

sun = rlight.create_light(rlight.LIGHT_DIRECTIONAL, rl.Vector3(0, 2, 2), rl.Vector3(0,0,0), rl.WHITE, shader)

def draw():
    global cam, winsize, iptojoin, ismenu, shouldquit, single, frame
    frame += 1
    shouldquit = rl.window_should_close()
    if not ismenu:
        return
    winsize = rl.Vector2(rl.get_screen_width(), rl.get_screen_height())
    cam = rl.update_camera(cam, rl.CAMERA_ORBITAL)
    rl.update_music_stream(music)
    rl.clear_background(rl.SKYBLUE)

    cameraPos = [cam.position.x, cam.position.y, cam.position.z]
    rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], cameraPos, rl.SHADER_UNIFORM_VEC3)

    rlight.update_light_values(shader, sun)

    rl.begin_mode_3d(cam)
    rl.begin_shader_mode(shader)

    rl.draw_model(bg, rl.Vector3(0,0,0), 1, rl.WHITE)
    #rl.draw_cube(rl.Vector3(0,0,0), 1, 1, 1, rl.RED)

    rl.end_shader_mode()
    rl.end_mode_3d()

    rl.draw_texture(logo, int(winsize.x / 2) - 150, int((int(winsize.y / 2) - 300) + math.sin(frame / 20) * 10), rl.WHITE)
    if rl.gui_button(rl.Rectangle(int(winsize.x / 2) - 150, int(winsize.y / 2) + 30, 300, 100), "Play"):
        if config.multiplayer:
            print(f"Trying to connect to {iptojoin}")
            try:
                connect.connectoserver(iptojoin)
            except:
                print("Failed to connect. Starting singleplayer world")
                shouldquit = True
                single = True
        else:
            shouldquit = True
            single = True
            
        
        rl.stop_music_stream(music)
        return
    if rl.gui_button(rl.Rectangle(int(winsize.x / 2) - 150, int(winsize.y / 2) + 200, 300, 100), "Quit"):
        shouldquit = True
    
    if config.multiplayer:
        if rl.is_key_down(rl.KEY_LEFT_SUPER) and rl.is_key_down(rl.KEY_V):
            iptojoin = rl.get_clipboard_text().decode()
        k, iptojoin = rl.gui_text_box(rl.Rectangle(int(winsize.x / 2) - 350, int(winsize.y / 2), 180, 50), iptojoin, 1024, True)
    else:
        rl.draw_text("Multiplayer is disabled", 10, 10, 20, rl.GRAY)