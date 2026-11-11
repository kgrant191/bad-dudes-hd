-- Exercise alternate truck CHR banks, blank tire animation cells and cab scroll.
local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local function frame()
 n=n+1
 if n%120==0 or (n>=590 and n<=660) or (n>=5200 and n<=5240) or (n>=7480 and n<=7560) then
  save(out..string.format('%05d.png',n),emu.takeScreenshot())
 end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then
  save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution()
 end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
