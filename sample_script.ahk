; WhatsApp Automation Script Template
; This is the base template used by the automation tool
; Variables enclosed in {variable_name} will be replaced with actual values

; Set custom icon for the script
; Use icon from the app instead of default AutoHotkey icon
#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SetBatchLines -1
CoordMode, Mouse, Screen

; Sleep time variables (milliseconds)
; These can be adjusted for troubleshooting
global sleep_1 := 1000  ; 1 second
global sleep_2 := 2000  ; 2 seconds
global sleep_3 := 3000  ; 3 seconds
global sleep_4 := 4000  ; 4 seconds

; ========== PHONE NUMBER PROCESSING TEMPLATE ==========
; This block will be repeated for each phone number

; Security check
Sleep {sleep_1}
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep {sleep_2}
Send !{Space}
Send {x}
Sleep {sleep_2}
Send !{d}
Sleep {sleep_1}
Send https://api.whatsapp.com/send/?phone={security_number}
Sleep {sleep_1}
Send {Enter}
Sleep {sleep_3}
MouseMove {coordinate_x},{coordinate_y}, 10
Sleep {sleep_4}
MouseClick, Left, {coordinate_x}, {coordinate_y}
Sleep {sleep_4}
Send +{phone_number}
Sleep {sleep_4}
Send {Enter}
Sleep {sleep_1}

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep {sleep_2}
Send !{Space}
Send {x}
Sleep {sleep_2}
Send !{d}
Sleep {sleep_1}
Send https://api.whatsapp.com/send/?phone={phone_number}
Sleep {sleep_1}
Send {Enter}
Sleep {sleep_4}

; Message Block 1
Sleep {sleep_1}
Send +{message_1}
Sleep {sleep_1}
Send {Enter}

; Message Block 2
Sleep {sleep_1}
Send +{message_2}
Sleep {sleep_1}
Send {Enter}

; Message Block 3
Sleep {sleep_1}
Send +{message_3}
Sleep {sleep_1}
Send {Enter}

; Message Block 4
Sleep {sleep_1}
Send +{message_4}
Sleep {sleep_1}
Send {Enter}

; ========== END PHONE NUMBER PROCESSING TEMPLATE ==========