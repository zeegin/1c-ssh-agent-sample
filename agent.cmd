set THICK_CLIENT="C:\Program Files\1cv8\current\bin\1cv8.exe"
set IB_CONNECTION_STRING="File=""C:\1c\db\demo"";"
set TEMP="C:\ssh-temp"

%THICK_CLIENT% DESIGNER ^
    /IBConnectionString %IB_CONNECTION_STRING% ^
    /AgentMode ^
    /AgentSSHHostKeyAuto ^
    /Visible ^
    /AgentBaseDir %TEMP%