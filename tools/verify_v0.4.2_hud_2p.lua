-- Diagnostic only: substitute the displayed label digit in nametable RAM.
-- This checks the 2P glyph rule without claiming a two-player gameplay replay.
local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(p,s) local f=assert(io.open(p,'wb'));f:write(s);f:close() end
local function frame()
 n=n+1
 if n>=90 then
  for a=0x2000,0x2ffe do
   if emu.read(a,emu.memType.nesPpuMemory)==0x81 and emu.read(a+1,emu.memType.nesPpuMemory)==0x9a then
    emu.write(a,0x82,emu.memType.nesPpuMemory)
   end
  end
 end
 if n==120 then
  save(out..'00120.png',emu.takeScreenshot())
  save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution()
 end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
