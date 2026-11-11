-- Diagnostic only: run with an isolated pack whose normal hero palettes are
-- swapped; force the second-hero flash selector. Never ship the diagnostic pack.
-- This validates artwork rendering, not a recorded player-two game.
local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local log=assert(io.open(out..'state.csv','w'))
local function frame()
 n=n+1
 local scene=emu.read(0x2c0,emu.memType.nesInternalRam)
 log:write(n..','..scene..'\n')
 if n==2136 or n==2172 or n==2448 or n==2598 or n==4452 or n==4464 or n==4554 or n==4758 then save(out..string.format('%05d.png',n),emu.takeScreenshot()) end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then log:close();save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)

emu.addEventCallback(function() emu.write(0x23f,1,emu.memType.nesInternalRam) end,emu.eventType.startFrame)
