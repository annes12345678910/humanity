import os
import props
import asset,math,config
from util import *
import ultimateraylib as rl
import pickle

__version__ = "0.0.1dev"

if os.path.exists("debug.log"):
    with open("debug.log", "w") as f:
        f.write('')

dumplog("LOGGING START")

dumplog(f"\nPlatform information: {rl.platform.platform()}")
dumplog(f"Raylib binding version: {rl.__version__}")
dumplog(f"Game Version: {__version__}\n")

dumplog("Camera Made")
cam = rl.make_camera(
    rl.Vector3(10,1.5,10),
    rl.Vector3(0,0,0),
    rl.Vector3(0,1,0),
    60,
    rl.CAMERA_PERSPECTIVE
)

rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)

rl.init_window(800, 600, "Singleplayer: Humanity")
dumplog(f"Initialized Window: Successful: {rl.is_window_ready()}")

rl.init_audio_device()
dumplog(f"Initialized Audio: Successful: {rl.is_audio_device_ready()}")

rl.set_target_fps(config.fps)
dumplog(f"Set fps to {config.fps}")

props.init()
# Load model + animations
headless = asset.load_model("assets/headless.glb")
headlessanim = asset.load_model_animations("assets/headless.glb")
#floor = rl.load_model("assets/floor.glb")
ok = rl.is_model_animation_valid(headless, headlessanim[0])
print("VALID?", ok)

m = headless.transform
print(
    m.m0, m.m1, m.m2, m.m3,
    m.m4, m.m5, m.m6, m.m7,
    m.m8, m.m9, m.m10, m.m11,
    m.m12, m.m13, m.m14, m.m15
)

tosave: dict = {}

frame = 0
current = 1     # current animation index
daynightf = 0
isnight = False
droppeditems = []

if os.path.exists(config.saveto):
    with open(config.saveto, "rb") as f:
        sdi = pickle.load(f)
        print(f"\nLoading {sdi}\n")
        daynightf = sdi["daynightf"]
        dia = sdi["droppeditems"]
        for i in dia:
            droppeditems.append(getattr(props, i['type'], "_empty")(listtovec3(i['pos']))) # type: ignore

        slots["left"] = getattr(props, sdi['slots']['left']['type'], "_empty")(listtovec3(sdi['slots']['left']['pos'])) if sdi['slots']['left'] else None # type: ignore

        slots["right"] = getattr(props, sdi['slots']['right']['type'], "_empty")(listtovec3(sdi['slots']['right']['pos'])) if sdi['slots']['right'] else None # type: ignore

        cam.position = listtovec3(sdi["playerpos"])

dumpandprint("=== ANIMATION DEBUG ===")
for anim in headlessanim:
    dumpandprint(f"Animation:, {anim.name}, frames:, {anim.frameCount}, bones:, {anim.boneCount}")
    for frame in range(min(3, anim.frameCount)):  # show first 3 frames
        root = anim.framePoses[frame][0]
        dumpandprint(f"Frame {frame}: pos={root.translation.x:.2f},{root.translation.y:.2f},{root.translation.z:.2f}  "
              f"rot={root.rotation.x:.2f},{root.rotation.y:.2f},{root.rotation.z:.2f},{root.rotation.w:.2f}  "
              f"scale={root.scale.x:.2f},{root.scale.y:.2f},{root.scale.z:.2f}")
dumpandprint("========================")

oooop = props.World()
drawemotes = False
freemusic = asset.load_music("assets/free.mp3")
#oooop.add_region(props.Region(rl.Vector3(0,0,0)))
#oooop.add_region(props.Region(rl.Vector3(32,0,0)))

currentframe = 0

while not rl.window_should_close():
    winw = rl.get_screen_width() if not rl.is_window_fullscreen() else rl.get_monitor_width(rl.get_current_monitor())
    winh = rl.get_screen_height() if not rl.is_window_fullscreen() else rl.get_monitor_height(rl.get_current_monitor())
    rl.update_camera(cam, rl.CAMERA_FIRST_PERSON)
    rl.set_mouse_position(int(winw / 2), int(winh / 2))
    
    #print(math.sin(currentframe))
    mouseray = rl.get_screen_to_world_ray(rl.get_mouse_position(), cam)
    cols = oooop.get_collision(mouseray)

    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        if cols and cols.pickable:
            if set67(cols.clas()):
                oooop.remove_object(cols)
                dumpandprint(f"Picked: {cols}")
        picked = []
        for i in droppeditems[:]:  # iterate over a copy
            if rl.get_ray_collision_box(mouseray, i.box).hit:
                if isinstance(i, props._empty) and not i.pickable:
                    continue
                if set67(i.clas() if isinstance(i, props._empty) else i):
                    picked.append(i)
                    dumpandprint(f"Picked dropped: {i}")  # or cols if properly defined

        # remove picked items after iteration
        for i in picked:
            droppeditems.remove(i)

    if rl.is_key_pressed(rl.KEY_C):
        craft()
    
    if rl.is_key_pressed(rl.KEY_Q):
        if isinstance(slots[config.dominanthand], props.Item) and not isinstance(slots[config.dominanthand], props.BuildingItem):
            erm: props.Item = slots[config.dominanthand] # type: ignore
            droppeditems.append(erm.blockform(model_pos) if erm.blockform else erm.__class__(model_pos))
            slots[config.dominanthand] = None
        elif isinstance(slots[nondominanthand], props.Item) and not isinstance(slots[nondominanthand], props.BuildingItem):
            erm: props.Item = slots[nondominanthand] # type: ignore
            if erm.hasblock:
                droppeditems.append(erm.blockform(model_pos) if erm.blockform else erm.__class__(model_pos))
            else:
                droppeditems.append(erm)
            slots[nondominanthand] = None
    
    if rl.is_key_pressed(rl.KEY_F):
        rl.toggle_fullscreen()



    anim = headlessanim[current]
    frame = (frame + 1) % anim.frameCount
    daynightf = (daynightf + 1) % 36000

    rl.update_music_stream(freemusic)
        
    if daynightf < 18000:
        if rl.is_music_stream_playing(freemusic):
            rl.stop_music_stream(freemusic)
        isnight = False
    else:
        if not drawemotes:
            if rl.is_key_pressed(rl.KEY_ONE):
                rl.play_music_stream(freemusic)
            if rl.is_key_pressed(rl.KEY_TWO):
                if rl.is_music_stream_playing(freemusic):
                    rl.stop_music_stream(freemusic)
        isnight = True
    
    if wasd() and not rl.is_key_down(rl.KEY_LEFT_SHIFT):
        current = 1
    elif rl.is_key_down(rl.KEY_LEFT_SHIFT) and wasd():
        current = 2
    elif current < 3:
        current = 0
    if rl.is_key_pressed(rl.KEY_PERIOD):
        drawemotes = not drawemotes
    
    # Place buildings
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
        dada = slots[config.dominanthand]
        if isinstance(dada, props.BuildingItem):
            buildings.append(dada.blockform(model_pos))
            slots[config.dominanthand] = None
    
    if drawemotes:
        if rl.is_key_pressed(rl.KEY_ONE):
            current = 3
        elif rl.is_key_pressed(rl.KEY_TWO):
            current = 4
        elif rl.is_key_pressed(rl.KEY_THREE):
            current = 5
    rl.update_model_animation(headless, anim, frame)
    #rl.update_model_animation_bones(headless, anim, frame)
    camyaw = get_camera_yaw(cam)
    rl.begin_drawing()
    rl.clear_background(rl.SKYBLUE)

    rl.begin_mode_3d(cam)
    #rl.draw_grid(100, 1)
    bb = rl.BoundingBox()
    #rl.Vector3(0,0,0)
    model_pos = rl.Vector3(cam.position.x + (0.1 if camyaw < -90 and camyaw > -180 else -0.1), (bb.min.y) if current == 0 else bb.min.y + 0.6, cam.position.z + (0.1 if camyaw < -90 and camyaw > -180 else -0.1))  # push mesh up by bottom Y

    oooop.ensure_region(snap_floor(model_pos))
    
    bb.min = rl.Vector3(model_pos.x - 0.3, model_pos.y if current == 0 else model_pos.y - 0.6, model_pos.z - 0.3)
    bb.max = rl.Vector3(model_pos.x + 0.3, (model_pos.y + 1.6) if current == 0 else model_pos.y + 1, model_pos.z + 0.3)
    rl.draw_model_ex(headless, model_pos, rl.Vector3(0,1,0), camyaw + 180, rl.Vector3(1,1,1), rl.WHITE)
    oooop.draw()
    for i in droppeditems:
        if isinstance(i, props._empty):
            i.draw()
        elif isinstance(i, props.Item):
            rl.draw_billboard(cam, i.texture, i.pos, 1, rl.WHITE)
            rl.draw_bounding_box(i.box, rl.RED)
    
    for i in buildings:
        if isinstance(i, props.Building):
            i.draw()

    #rl.draw_ray(mouseray, rl.RED)
    rl.end_mode_3d()
    rl.draw_text(str(daynightf), 0, 0, 20, rl.BLACK)
    if drawemotes:
        rl.draw_rectangle(int(winw / 2) - 200, int(winh / 2) - 200, 400, 400, rl.LIGHTGRAY)
        rl.draw_text("\nPress 2 for dance1\nPress 3 for flex", int(winw / 2) - 190, int(winh / 2) - 190, 20, rl.BLACK)
    
    if isinstance(cols, props._empty):
        if cols.pickable and handsfree():
            rl.draw_text(f"Click To Pickup {cols.__class__.__name__.capitalize()}", int(winw / 2) - 50, int(winh / 2) - 30, 20, rl.BLACK)
        elif cols.pickable and slots["left"] and slots["right"]:
            rl.draw_text("Your hands are full", int(winw / 2) - 50, int(winh / 2) - 30, 20, rl.BLACK)
    
    for i in droppeditems[:]:  # iterate over a copy
        if rl.get_ray_collision_box(mouseray, i.box).hit:
            if isinstance(i, props._empty) and i.pickable:
                continue
            if handsfree():
                rl.draw_text(f"Click To Pickup {i.__class__.__name__.capitalize()}", int(winw / 2) - 50, int(winh / 2) - 30, 20, rl.BLACK)
            else:
                rl.draw_text("Your hands are full", int(winw / 2) - 50, int(winh / 2) - 30, 20, rl.BLACK)
        
    if isinstance(slots["left"], props.Item):
        slots["left"].draw(rl.Vector2(10, winh - 74)) # type: ignore
        rl.draw_text("Left Hand", 10, winh - 94, 20, rl.BLACK)
    
    if isinstance(slots["right"], props.Item):
        slots["right"].draw(rl.Vector2(winw - 74, winh - 74)) # type: ignore
        rl.draw_text("Right Hand", winw - 124, winh - 94, 20, rl.BLACK)
    rl.end_drawing()

    tosave = {
        "daynightf": daynightf,
        "droppeditems": [],
        "playerpos": vec3tolist(cam.position),
        "world": oooop.todict(),
        "slots": {
            "left": slots["left"].todict() if isinstance(slots["left"], props.Item) else None,
            "right": slots["right"].todict() if isinstance(slots["right"], props.Item) else None
                  }
    }
    for i in droppeditems:
        tosave["droppeditems"].append(i.todict())

dumplog(f'Saved Progress to "{config.saveto}" it is {tosave}')
with open(config.saveto, "wb") as f:
    pickle.dump(tosave, f)

dumplog("Quitting")
rl.close_window()
rl.close_audio_device()