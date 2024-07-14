#Requires AutoHotkey v2.0

; Initialize global variables
global isJiggling := false

; Create the GUI
MyGui := Gui()
MyGui.Title := "BetterJiggler by TJ (v2)"
MyGui.Opt("+AlwaysOnTop -Caption")

; Add a draggable area
dragArea := MyGui.Add("Text", "w210 h10 x0 y0 BackgroundSilver")
dragArea.GetPos(&dragX, &dragY, &dragW, &dragH)
dragArea.OnEvent("Click", GuiDrag)

; Add the status box
statusBox := MyGui.Add("Progress", "w30 h30 x10 y20 Background808080")
statusBox.Opt("Background880000")  ; Start with red color (jiggle off)

; Add the start/stop button
toggleButton := MyGui.Add("Button", "w80 h30 x50 y20", "Start")
toggleButton.OnEvent("Click", ToggleJiggle)

; Add the minimize button
minimizeButton := MyGui.Add("Button", "w30 h30 x140 y20", "_")
minimizeButton.OnEvent("Click", MinimizeGui)

; Add the close button
closeButton := MyGui.Add("Button", "w30 h30 x170 y20", "X")
closeButton.OnEvent("Click", (*) => ExitApp())

; Show the GUI
MyGui.Show("w210 h60")

; Function to make the window draggable
GuiDrag(*)
{
    PostMessage(0xA1, 2, , , "A")
}

; Toggle jiggle function
ToggleJiggle(*)
{
    global isJiggling, statusBox, toggleButton

    isJiggling := !isJiggling
    if (isJiggling)
    {
        statusBox.Opt("Background008800")  ; Green
        toggleButton.Text := "Stop"
        SetTimer(Jiggle, 1000)
    }
    else
    {
        statusBox.Opt("Background880000")  ; Red
        toggleButton.Text := "Start"
        SetTimer(Jiggle, 0)  ; Turn off the timer
    }
}

; Jiggle function
Jiggle()
{
    MouseMove(3, 0, 0, "R")  ; Move right 3 pixels
    Sleep(10)
    MouseMove(-3, 0, 0, "R")  ; Move left 3 pixels
}

; Minimize function
MinimizeGui(*)
{
    MyGui.Minimize()
}

; Exit script when GUI is closed
MyGui.OnEvent("Close", (*) => ExitApp())