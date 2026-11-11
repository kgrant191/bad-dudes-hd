local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local function frame()
 n=n+1
 if n%120==0 then
  save(out..string.format('%05d.png',n),emu.takeScreenshot())
  save(out..string.format('%05d.ram',n),string.char(emu.read(0x2c0,emu.memType.nesInternalRam)))
 end
 if n>=8500 then save(assert(os.getenv('BAD_DUDES_HOME'))..'/done','done');emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
