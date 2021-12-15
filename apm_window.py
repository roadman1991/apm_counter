import threading
import time

import win32api
import win32con
import win32gui
import win32ui

apm_text = 'none'
hWindow = ''
def apm_window():
    hInstance = win32api.GetModuleHandle()
    className = 'MyWindowClassName'
    wndClass = win32gui.WNDCLASS()
    wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc = wndProc
    wndClass.hInstance = hInstance
    wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName = className
    wndClassAtom = win32gui.RegisterClass(wndClass)

    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

    style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE
    hWindow = win32gui.CreateWindowEx(
        exStyle,
        wndClassAtom,
        None,  # WindowName
        style,
        0,  # x
        0,  # y
        win32api.GetSystemMetrics(win32con.SM_CXSCREEN),  # width
        win32api.GetSystemMetrics(win32con.SM_CYSCREEN),  # height
        None,  # hWndParent
        None,  # hMenu
        hInstance,
        None  # lpParam
    )
    win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
    win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    win32gui.UpdateWindow(hWindow)

    # New code: Create and start the thread
    thr = threading.Thread(target=custom_draw, args=(hWindow,))
    thr.setDaemon(False)
    thr.start()
    win32gui.PumpMessages()


def custom_draw(hWindow):
    global apm_text
    time.sleep(1.0)
    apm_text = 'something_new'
    win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)


def wndProc(hWnd, message, wParam, lParam):
    if message == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hWnd)

        dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
        fontSize = 80

        # http://msdn.microsoft.com/en-us/library/windows/desktop/dd145037(v=vs.85).aspx
        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Times New Roman"
        lf.lfHeight = int(round(dpiScale * fontSize))
        # lf.lfWeight = 150
        # Use nonantialiased to remove the white edges around the text.
        # lf.lfQuality = win32con.NONANTIALIASED_QUALITY
        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hdc, hf)
        rect = win32gui.GetClientRect(hWnd)
        # http://msdn.microsoft.com/en-us/library/windows/desktop/dd162498(v=vs.85).aspx
        win32gui.DrawText(
            hdc,
            apm_text,
            -1,
            rect,
            win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER
        )

        win32gui.EndPaint(hWnd, paintStruct)
        return 0

    elif message == win32con.WM_DESTROY:
        print('Closing the window.')
        win32gui.PostQuitMessage(0)
        return 0

    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)


def set_apm_text(text):
    global apm_text
    apm_text = text