from cx_Freeze import setup, Executable

target = Executable(
    script='Restaurant.py',
    base='Win32GUI',
    icon='Restaurant.ico'

)

setup(
    name='Restaurant',
    version='1.0',
    description='Restaurant Application',
    executables=[target]
)
