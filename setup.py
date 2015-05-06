from distutils.core import setup
import py2exe

script = [
    {
        "script": "apps/graph/main_window.py"
    }
]

py2exe_opciones = {
    "py2exe": {
        "dll_excludes": ["MSVCP90.dll"],
        "includes": ["sip"]
    }
}

setup(windows=script, options=py2exe_opciones)