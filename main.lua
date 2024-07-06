print("finding")
local TargetPartName = "Head"
local DrawTeammates = false -- set to false to save external rendering performance
local FindHumanoids = false -- VERYY LAGGY
local datapath = "drawingdata/data.json"
local settingspath = "drawingdata/settings.json"
local Players = game:GetService("Players")


-- Some executors can run before replicatedfirst, so that needs to be accounted for.
local LocalPlayer = Players.LocalPlayer or Players:GetPropertyChangedSignal("LocalPlayer"):Wait() 
local Camera = workspace.CurrentCamera or workspace:GetPropertyChangedSignal("CurrentCamera"):Wait()

-- CurrentCamera can change
workspace:GetPropertyChangedSignal("CurrentCamera"):Connect(function(NewCamera)
    Camera = NewCamera
end)

local HttpService = game:GetService("HttpService")

local function GetCorners(Part)
    local CF, Size, Corners = Part.CFrame, Part.Size / 2, {};
    for X = -1, 1, 2 do for Y = -1, 1, 2 do for Z = -1, 1, 2 do
        Corners[#Corners+1] = (CF * CFrame.new(Size * Vector3.new(X, Y, Z))).Position;      
    end; end; end;
    return Corners;
end

while true do

    local Targets = {}
    for _, Player in pairs(game.Players:GetPlayers()) do
        if Player == game.Players.LocalPlayer then
            continue
        end
        local IsTeammate = game.Players.LocalPlayer.Team and Player.Team == game.Players.LocalPlayer.Team
        if not DrawTeammates and IsTeammate then
            continue
        end
        local Character = Player.Character
        if not Character then
            print("no char")
            continue
        end
        local TargetPart = Character:FindFirstChild(TargetPartName)
        if not TargetPart then
            continue
        end
        local ScreenPoint, OnScreen = Camera:WorldToScreenPoint(TargetPart.Position)
        if OnScreen then
            table.insert(Targets, {Vector2.new(ScreenPoint.X, ScreenPoint.Y), tostring(TargetPart.Parent.Name),(Camera.CFrame.Position - TargetPart.Position).Magnitude})
        end
    end

    local cached = "["
    local first = true
    for _, Target in pairs(Targets) do
        if not first then
            cached = cached .. ","
        end
        cached = cached .. '{"X":' .. tostring(Target[1].X) .. ', "Y":' .. tostring(Target[1].Y) .. ', "name":"' .. Target[2] .. '", "Distance": '..math.round(Target[3])..'}'
        first = false
    end
    cached = cached .. "]"
    
    writefile(datapath, cached)
    --task.spawn(writefile, path, HttpService:JSONEncode(Targets)) --task.spawn is buggy
    task.wait() 
end

warn("Exited") -- This line will only execute if the script exits the while loop, not normally during execution
