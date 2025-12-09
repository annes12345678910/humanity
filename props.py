import random,asset
import ultimateraylib as rl
import math,util

def init():
    global treemodel, floormodel, rockmodel, tree_bb, rock_bb, flintmodel, flint_bb,rocktex, itemtex, flinttex, craftsound, knifetex, buildingmodel, building_bb, buildingtex, smilodonmodel, smilodonanims, suntex
    treemodel = asset.load_model("assets/tree.glb")
    floormodel = asset.load_model("assets/floor.glb")
    rockmodel = asset.load_model("assets/rock.glb")
    flintmodel = asset.load_model("assets/flint.glb")

    tree_bb = rl.get_model_bounding_box(treemodel)
    rock_bb = rl.get_model_bounding_box(rockmodel)
    flint_bb = rl.get_model_bounding_box(flintmodel)

    rocktex = asset.load_texture("assets/rockitem.png")
    flinttex = asset.load_texture("assets/flintitem.png")
    itemtex = asset.load_texture("assets/ITEM.png")

    craftsound = asset.load_sound("assets/craft.mp3")

    knifetex = asset.load_texture("assets/knife.png")

    buildingmodel = asset.load_model("assets/building.glb")
    building_bb = rl.get_model_bounding_box(buildingmodel)
    buildingtex = asset.load_texture("assets/building.png")

    smilodonmodel = asset.load_model("assets/smilodon.glb")
    smilodonanims = asset.load_model_animations("assets/smilodon.glb")

    suntex = asset.load_texture("assets/sun.png")

class Animal:
    def __init__(self, health: int, model: rl.Model, modelanims: list[rl.ModelAnimation] | None, pos: rl.Vector3, roty: float) -> None:
        self.health = health
        self.model = model
        self.modelanims = modelanims
        self.animframe = 0
        self.index = 0
        self.sheetindex = 0
        self.pos = pos
        self.roty = roty  # rotation around Y axis in degrees
        self.box = rl.get_model_bounding_box(self.model)
        self._updateboxpos()
        
    def _updateboxpos(self):
        """Update the bounding box position so its bottom is at self.pos."""
        # Compute width/depth offsets
        width = self.box.max.x - self.box.min.x
        depth = self.box.max.z - self.box.min.z
        height = self.box.max.y - self.box.min.y

        # Position the box so its bottom is at self.pos
        self.box.min.x = self.pos.x - width / 2
        self.box.min.y = self.pos.y
        self.box.min.z = self.pos.z - depth / 2

        self.box.max.x = self.pos.x + width / 2
        self.box.max.y = self.pos.y + height
        self.box.max.z = self.pos.z + depth / 2


    def moveto(self, target: rl.Vector3, speed: float = 0.1, rot_speed: float = 2.0):
        # Compute the direction vector from current pos to target
        dir_x = target.x - self.pos.x
        dir_z = target.z - self.pos.z
        
        # Compute the desired rotation (angle in degrees)
        desired_angle = math.degrees(math.atan2(dir_x, dir_z))  # atan2(x, z) for Y-up coordinates
        
        # Smoothly rotate towards target
        angle_diff = (desired_angle - self.roty + 180) % 360 - 180  # shortest rotation
        self.roty += max(min(angle_diff, rot_speed), -rot_speed)  # clamp by rot_speed

        # Compute movement in the forward direction
        rad = math.radians(self.roty)
        forward_x = math.sin(rad)
        forward_z = math.cos(rad)
        
        # Move towards the target slowly
        distance = math.sqrt(dir_x**2 + dir_z**2)
        move_step = min(speed, distance)  # don't overshoot
        self.pos.x += forward_x * move_step
        self.pos.z += forward_z * move_step
        self._updateboxpos()
        if distance < 0.01:
            return True
        return False


    def draw(self, debug=False):
        if self.modelanims:
            self.animframe = (self.animframe + 1) % self.modelanims[self.index].frameCount
            rl.update_model_animation(self.model, self.modelanims[self.index], self.animframe)

        rl.draw_model_ex(
            self.model, 
            self.pos, 
            rl.Vector3(0, 1, 0), 
            self.roty + 180, 
            rl.Vector3(1, 1, 1), 
            rl.WHITE
        )
        if debug:
            rl.draw_bounding_box(self.box, rl.RED)
            rl.draw_model_wires_ex(
            self.model, 
            self.pos, 
            rl.Vector3(0, 1, 0), 
            self.roty + 180, 
            rl.Vector3(1, 1, 1), 
            rl.BLACK
            )
    
    def followmovesheet(self, sheet: list[rl.Vector3], speed=0.1, rotspeed=2, loop=False):
        """Follow a sheet of moves."""
        
        if not sheet:
            return

        target = sheet[self.sheetindex]

        # Move toward target, returns True if reached
        if self.moveto(target, speed, rotspeed):
            # Increment index
            if self.sheetindex < len(sheet) - 1:
                self.sheetindex += 1
            elif loop:
                self.sheetindex = 0
            # If not looping and at last target, stay there
    
    def checkcollision(self, other):
        return rl.check_collision_boxes(self.box, other.box)



class _empty:
    def __init__(self, pos=rl.Vector3(0,0,0)) -> None:
        self.box = rl.BoundingBox()
        self.pos = pos
        self.pickable = False
        self.clas = Item
    def update_box(self, withh):
        self.box.min = rl.Vector3(
            withh.min.x + self.pos.x,
            withh.min.y + self.pos.y,
            withh.min.z + self.pos.z
        )
        self.box.max = rl.Vector3(
            withh.max.x + self.pos.x,
            withh.max.y + self.pos.y,
            withh.max.z + self.pos.z
        )

    def draw(self):
        pass

    def todict(self):
        return {"type":self.__class__.__name__, "pos": util.vec3tolist(self.pos)}
        

class Tree(_empty):
    def __init__(self, pos=rl.Vector3(0, 0, 0)):
        super().__init__(pos)

        # apply the tree's position (translation)
        self.update_box(tree_bb)

    def draw(self):
        rl.draw_model(treemodel, self.pos, 1, rl.WHITE)
        rl.draw_bounding_box(self.box, rl.RED)


class Rock(_empty):
    def __init__(self, pos=rl.Vector3(0, 0, 0)) -> None:
        super().__init__(pos)
        self.update_box(rock_bb)
        self.pickable = True
        self.clas = RockItem

    def draw(self):
        rl.draw_model(rockmodel, self.pos, 1, rl.WHITE)
        rl.draw_bounding_box(self.box, rl.RED)

class Flint(_empty):
    def __init__(self, pos=rl.Vector3(0, 0, 0)) -> None:
        super().__init__(pos)
        self.update_box(flint_bb)
        self.pickable = True
        self.clas = FlintItem
    def draw(self):
        rl.draw_model(flintmodel, self.pos, 1, rl.WHITE)
        rl.draw_bounding_box(self.box, rl.RED)

CELL_SIZE = 1.0  # or whatever size your world uses

class Region:
    def __init__(self, pos: rl.Vector3):
        self.items = []
        self.pos = pos

        # Generate the 2D grid
        for _ in range(32):
            row = [random.randint(0, 70) for _ in range(32)]
            self.items.append(row)

        # Replace all 10s with Trees at their proper world position
        for r, row in enumerate(self.items):
            for c, val in enumerate(row):
                world_x = c * CELL_SIZE
                world_z = r * CELL_SIZE
                world_y = 0
                if val == 10:
                    self.items[r][c] = Tree(rl.Vector3(world_x + self.pos.x, world_y + self.pos.y, world_z + self.pos.z))
                elif val == 20:
                    self.items[r][c] = Rock(rl.Vector3(world_x + self.pos.x, world_y + self.pos.y, world_z + self.pos.z))
                elif val == 5:
                    self.items[r][c] = Flint(rl.Vector3(world_x + self.pos.x, world_y + self.pos.y, world_z + self.pos.z))
                else:
                    self.items[r][c] = _empty()
        for i in self.items:
            for o in i:
                if not o.__class__ == _empty:
                    print("Something at row:", self.items.index(i), "Colume:", i.index(o), "it is:", o, "Position:", o.pos.x, o.pos.y, o.pos.z)

    def draw(self):
        rl.draw_model(floormodel, rl.Vector3(self.pos.x + 16, self.pos.y, self.pos.z + 16), 1, rl.WHITE)
        for i in self.items:
            for o in i:
                o.draw()
    def checkcollisions(self, ray: rl.Ray, distance = 12):
        for i in self.items:
            for o in i:
                col = rl.get_ray_collision_box(ray, o.box)
                #print(col.distance)
                if col.hit and col.distance <= distance:
                    if not o.__class__ == _empty:
                        return o
        return None
    def remove_object(self, obj):
        for r in range(len(self.items)):
            for c in range(len(self.items[r])):
                if self.items[r][c] is obj:
                    self.items[r][c] = _empty()
                    return True
        return False
    def todict(self):
        dad:dict = {}
        dad['pos'] = util.vec3tolist(self.pos)
        dad['items'] = []
        for i in self.items:
            rar = []
            for o in i:
                rar.append(o.todict())
            #print(rar)
            dad["items"].append(rar)


        #print(dad)
        return dad



REGION_SIZE = 32 * CELL_SIZE   # one region covers a 32×32 grid
def region_coord(v: rl.Vector3):
    return (
        int(v.x) // 32,
        int(v.y) // 32,
        int(v.z) // 32
    )

class World:
    def __init__(self, region_size=32, cell_size=1):
        self.region_size = region_size
        self.cell_size = cell_size
        self.regions = {}     # (rx, rz) → Region

    def add_region(self, region: Region):
        rc = (int(region.pos.x), int(region.pos.z))
        self.regions[rc] = region
        return region

    def draw(self):
        for region in self.regions.values():
            region.draw()

    def get_collision(self, ray: rl.Ray, distance=12):
        closest_obj = None
        closest_dist = distance

        for region in self.regions.values():
            obj = region.checkcollisions(ray, distance)
            if obj:
                col = rl.get_ray_collision_box(ray, obj.box)
                if col.hit and col.distance < closest_dist:
                    closest_obj = obj
                    closest_dist = col.distance

        return closest_obj

    def remove_object(self, obj):
        for region in self.regions.values():
            if region.remove_object(obj):
                return True
        return False

    def ensure_region(self, pos: rl.Vector3):
        rpos = region_coord(pos)  # (rx, rz)

        if rpos not in self.regions:
            # Create the new region at coordinate (rx, rz)
            world_pos = rl.Vector3(rpos[0], 0, rpos[1])
            new_region = Region(pos)
            self.regions[rpos] = new_region
            print(f"I discovered {new_region}, new map is {self.regions}")
        return self.regions[rpos]

    def todict(self):
        dad:dict = {}

        opo:dict = {}
        for i, o in self.regions.items():
            opo[str(i)] = o.todict()

        dad["regions"] = opo

        return dad




class Item:
    def __init__(self, pos=rl.Vector3()) -> None:
        self.takesdamage = False
        self.durability = 10 # how much the item can be used
        self.texture =  itemtex
        self.pos = pos
        self.hasblock = False
        self.blockform = None
        self.box = rl.BoundingBox()
        opo = 0.3
        self.box.min = rl.vector3_subtract(self.pos, rl.Vector3(opo, opo, opo))
        self.box.max = rl.vector3_add(self.pos, rl.Vector3(opo, opo, opo))

        "should be 32x32 texture"
        
    def draw(self, pos: rl.Vector2):
        rl.draw_texture_ex(self.texture, pos, 0, 2, rl.WHITE)

    def todict(self):
        return {"type":self.__class__.__name__, "pos": util.vec3tolist(self.pos)}

class RockItem(Item):
    def __init__(self, pos=rl.Vector3()) -> None:
        super().__init__(pos)
        self.texture = rocktex
        self.hasblock = True
        self.blockform = Rock

class FlintItem(Item):
    def __init__(self, pos=rl.Vector3()) -> None:
        super().__init__(pos)
        self.texture = flinttex
        self.hasblock = True
        self.blockform = Flint

class Knife(Item):
    def __init__(self, pos=rl.Vector3()) -> None:
        super().__init__(pos)
        self.texture = knifetex

class Building:
    def __init__(self, pos=rl.Vector3()) -> None:
        self.pos = pos
        self.box = rl.BoundingBox()
        self.health = 10
        self.update_box(building_bb)

    def update_box(self, withh):
        self.box.min = rl.Vector3(
            withh.min.x + self.pos.x,
            withh.min.y + self.pos.y,
            withh.min.z + self.pos.z
        )
        self.box.max = rl.Vector3(
            withh.max.x + self.pos.x,
            withh.max.y + self.pos.y,
            withh.max.z + self.pos.z
        )
    
    def draw(self):
        rl.draw_model(buildingmodel, self.pos, 1, rl.WHITE)
        rl.draw_bounding_box(self.box, rl.RED)

class BuildingItem(Item):
    def __init__(self, pos=rl.Vector3()) -> None:
        super().__init__(pos)
        self.blockform = Building
        self.texture = buildingtex
    

def test():
    rl.init_window()
    init()
    
    ada = Region(rl.Vector3(0,0,0))
    util.dicttoregion(ada.todict())
    rl.close_window()

if __name__ == "__main__":
    test()