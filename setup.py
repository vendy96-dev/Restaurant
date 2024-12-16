from cx_Freeze import setup, Executable

target = Executable(
    script='Restaurant-to-build.py',
    base='Win32GUI',
    icon='Restaurant.ico'

)

setup(
    name='Restaurant',
    version='1.0',
    description='Restaurant Application',
    executables=[target],
    options={
        "build_exe":{
            "packages":["sqlite3","datetime","customtkinter","tkinter","logging"],
            "include_files":["Restaurant.ico","Restaurant.png","python310.dll", "api-ms-win-core-path-l1-1-0.dll", "user_db.db", "menu_db.db","orders_db.db","readme.txt"]
        }
    }
)
