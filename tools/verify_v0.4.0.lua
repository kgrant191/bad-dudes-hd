local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local chosen={ [941]=true,[943]=true,[3386]=true,[3388]=true,[3404]=true,[3406]=true,[4621]=true,[4623]=true,[4626]=true,[4628]=true,[4701]=true,[4703]=true,[4732]=true,[4734]=true }
local function save(p,s) local f=assert(io.open(p,'wb'));f:write(s);f:close() end
local function frame()
 n=n+1
 if n%120==0 or chosen[n] or (n>=1200 and n<=1380 and n%4==0) or (n>=4590 and n<=4750 and n%4==0) then
  save(out..string.format('%05d.png',n),emu.takeScreenshot())
 end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
