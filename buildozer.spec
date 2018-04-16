[app]

# (str) Title of your application
title = androidserver2

# (str) Package name
package.name = Android_Server_2

# (str) Package domain (needed for android/ios packaging)
package.domain = labomedia.org

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,ini

# (str) Application versioning (method 1)
version=0.75

# 0.75 sans accent ok
# 0.74 kivy,twisted ok
# 0.73 incremental,kivy,twisted bad
# 0.72 incremental,kivy, incremental dans python2.7
# 0.71 incremental, pas de dossier incremental obtenu

# (list) Application requirements
# comma seperated e.g. requirements = sqlite3,kivy
requirements=kivy,twisted

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for new android toolchain)
android.presplash_color = fuchsia

# (list) Permissions ,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.permissions = INTERNET,CHANGE_WIFI_MULTICAST_STATE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86
android.arch = armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 1

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
