local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local log=assert(io.open(out..'state.csv','w'))
local function frame()
 n=n+1
 local scene=emu.read(0x2c0,emu.memType.nesInternalRam)
 log:write(n..','..scene..'\n')
 if n%30==0 or (n<=240 and n%6==0) or (n>=1850 and n<=2200 and n%6==0) or (n>=2400 and n<=2650 and n%6==0) or (n>=3900 and n<=3950 and n%6==0) or (n>=4400 and n<=4800 and n%6==0) or (n>=6120 and n<=6310 and n%6==0) or (n>=7330 and n<=8350 and n%6==0) then save(out..string.format('%05d.png',n),emu.takeScreenshot()) end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then log:close();save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
