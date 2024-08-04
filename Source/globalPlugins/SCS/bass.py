import os;
import ctypes;
module_dir = os.path.dirname(__file__);
bassdll= os.path.join(module_dir, "bass.dll");

bass = ctypes.WinDLL(bassdll);

bass.BASS_Init.argtypes = [ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p];
bass.BASS_Init.restype = ctypes.c_bool;

bass.BASS_Init(-1, 44100, 0, None, None);
def play(sound=str):

    bass.BASS_StreamCreateFile.argtypes = [ctypes.c_bool, ctypes.c_void_p, ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_uint];
    bass.BASS_StreamCreateFile.restype = ctypes.c_uint;
    stream_handle = bass.BASS_StreamCreateFile(False, sound.encode('utf-8'), 0, 0, 0);
    bass.BASS_ChannelPlay.argtypes = [ctypes.c_uint, ctypes.c_bool];
    bass.BASS_ChannelPlay.restype = ctypes.c_bool;
    bass.BASS_ChannelPlay(stream_handle, True);