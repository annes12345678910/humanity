import ultimateraylib as rl
rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
rl.init_window(800, 1000, "Humanity")
rl.init_audio_device()
rl.set_exit_key(rl.KEY_NULL)
rl.set_target_fps(60)
import menu

while not menu.shouldquit:
    rl.begin_drawing()
    menu.draw()
    rl.end_drawing()

print("Meow")
#rl.close_window()
#rl.close_audio_device()
