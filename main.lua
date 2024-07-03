local TargetPartName = "Head"
local DrawTeammates = true
local FindHumanoids = false -- TODO
local path = "drawingdata/data.json"

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")

-- Some executors can run before replicatedfirst, so that needs to be accounted for.
local LocalPlayer = Players.LocalPlayer or Players:GetPropertyChangedSignal("LocalPlayer"):Wait() 
local Camera = workspace.CurrentCamera or workspace:GetPropertyChangedSignal("CurrentCamera"):Wait()

-- CurrentCamera can change
workspace:GetPropertyChangedSignal("CurrentCamera"):Connect(function(NewCamera)
    Camera = NewCamera
end)

local Targets = {}

while true do
    if not Camera then
        continue
    end

    table.clear(Targets)

    for i, Player in Players:GetPlayers() do
        if i == 1 then -- LocalPlayer is always idx 1
            continue
        end

        local Team = Player.Team
        local Character = Player.Character
        local Part = Character and Character:FindFirstChild(TargetPartName) -- If character is nil, Part is nil. Prevents errors 

        if (not Part) or (Team == LocalPlayer.Team and not DrawTeammates) then
           continue 
        end

        local Position, OnScreen = Camera:WorldToViewportPoint(Part.Position)

        if OnScreen then
            table.insert(Targets, {
                X = Position.X,
                Y = Position.Y,
                name = Player.Name,
                Distance = (Camera.CFrame.Position - Position).Magnitude
            })
        end
    end

    if #Targets > 0 then
        task.spawn(writefile, path, HttpService:JSONEncode(Targets))
    end
    
    RunService.Heartbeat:Wait()
end
