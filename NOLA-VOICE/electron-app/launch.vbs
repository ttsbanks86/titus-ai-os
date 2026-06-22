Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = """C:\Users\tbank\Desktop\Live Cowork\ECHOKEYS\electron-app"""
WshShell.Run """C:\Users\tbank\Desktop\Live Cowork\ECHOKEYS\electron-app\node_modules\electron\dist\electron.exe"" """ & """C:\Users\tbank\Desktop\Live Cowork\NOLA-VOICE\electron-app""" & """", 0, False
