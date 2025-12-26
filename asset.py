import ultimateraylib as rl
from pathlib import Path

parent = Path(__file__).parent

def _format(string: str):
    return f"{str(parent)}/{string}"

def load_model(path: str):
    return rl.load_model(_format(path))

def load_texture(path: str):
    return rl.load_texture(_format(path))

def load_sound(path: str):
    return rl.load_sound(_format(path))

def load_music(path: str):
    return rl.load_music_stream(_format(path))

def load_model_animations(path:str):
    return rl.load_model_animations(_format(path))

def load_shader(vs:str, fs:str):
    return rl.load_shader(_format(vs), _format(fs))
