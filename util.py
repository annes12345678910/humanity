import math,config,sys,props
import ultimateraylib as rl
wasdspeed = rl.Vector2(0,0)

nondominanthand = ""

if config.dominanthand == "left":
    nondominanthand = "right"
elif config.dominanthand == "right":
    nondominanthand = "left"

slots = {
    "left": None,
    "right": None
}
def handsfree():
    if not slots["left"] or not slots["right"]:
        return True
    return False

def listtovec3(lis: list):
    return rl.Vector3(lis[0], lis[1], lis[2])

def vec3tolist(vec3: rl.Vector3):
    return [vec3.x, vec3.y, vec3.z]

def boxtodict(box: rl.BoundingBox):
    return {
        "min":vec3tolist(box.min),
        "max":vec3tolist(box.max)
    }

def dumplog(string: str, sep:str = '\n'):
    with open("debug.log", "a") as f:
        f.write(string + sep)
def dumpandprint(string: str, sep:str = '\n'):
    dumplog(string, sep)
    print(string, end=sep)

def get_camera_yaw(cam: rl.Camera) -> float:
    # Direction vector from camera to target
    dir_x = cam.target.x - cam.position.x
    dir_z = cam.target.z - cam.position.z
    
    # atan2 returns angle in radians; convert to degrees
    yaw = math.degrees(math.atan2(dir_x, dir_z))
    return yaw

def wasd():
    if rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_S):
        return True
    return False

def set67(value):
    dominant = config.dominanthand
    nondominant = nondominanthand

    # If dominant is free → use it
    if not slots.get(dominant):
        slots[dominant] = value
        return True

    # If dominant is full but nondominant is free → use nondominant
    if not slots.get(nondominant):
        slots[nondominant] = value
        return True

    # Both hands full → no available slot
    return False

def slotsare(class1, class2):
    'class1 = left, class2 = right'
    if isinstance(slots["left"], class1) and isinstance(slots["right"], class2):
        return True
    return False

def bothslotsare(value):
    if slots[config.dominanthand] == value and slots[nondominanthand] == value:
        return True
    return False

def handshave(value1, value2):
    a = slots[config.dominanthand].__class__ == value1 or slots[config.dominanthand].__class__ == value2
    b = slots[nondominanthand].__class__ == value1 or slots[nondominanthand].__class__ == value2
    if slots[config.dominanthand].__class__ == slots[nondominanthand].__class__:
        return False
    return a == b

def clearhands():
    slots[config.dominanthand] = None
    slots[nondominanthand] = None

def snap_vector3(vec: rl.Vector3, grid=32):
    return rl.Vector3(
        round(vec.x / grid) * grid,
        round(vec.y / grid) * grid,
        round(vec.z / grid) * grid
    )


def snap_floor(vec: rl.Vector3, grid=32):
    return rl.Vector3(
        math.floor(vec.x / grid) * grid,
        math.floor(vec.y / grid) * grid,
        math.floor(vec.z / grid) * grid
    )

def dicttoregion(dik: dict):
    ada = props.Region(listtovec3(dik["pos"]))
    items = dik["items"]
    #print(items)
    for item in items:
        getattr(props, item['type'], "_empty")(listtovec3(item['pos'])) # type: ignore

def craft():
    crafted = None
    if handshave(props.RockItem, props.FlintItem):
        rl.play_sound(props.craftsound)
        clearhands()
        #slots[config.dominanthand] = props.Knife() # type: ignore
        set67(props.Knife())
        crafted = slots[config.dominanthand]
    
    dumpandprint(f"I crafted {crafted}")
    