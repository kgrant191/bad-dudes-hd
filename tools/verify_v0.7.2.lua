local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local log=assert(io.open(out..'state.csv','w'))
local function frame()
 n=n+1
 log:write(n..','..emu.read(0x2c0,emu.memType.nesInternalRam)..'\n')
 if n%30==0 or (n>=540 and n<=710 and n%2==0) then save(out..string.format('%05d.png',n),emu.takeScreenshot()) end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then log:close();save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
