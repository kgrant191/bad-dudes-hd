local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local chosen={ [120]=true,[510]=true,[570]=true,[722]=true,[1020]=true,[1800]=true,[2356]=true,[2360]=true,[2370]=true,[2430]=true,[2437]=true,[2438]=true,[2440]=true,[2460]=true,[3000]=true,[3300]=true,[3840]=true,[4890]=true,[5100]=true,[5400]=true,[6000]=true,[6180]=true,[6360]=true,[6600]=true,[7290]=true,[7800]=true,[8160]=true,[8370]=true }
local function save(p,s) local f=assert(io.open(p,'wb'));f:write(s);f:close() end
local function frame()
 n=n+1
 if chosen[n] then save(out..string.format('%05d.png',n),emu.takeScreenshot()) end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
