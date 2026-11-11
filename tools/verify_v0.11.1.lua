-- Replay screenshots and state checks for the player/lives menu correction.
-- MENU_GLYPH_DIAGNOSTIC is display-only: substitute nametable digits while
-- the recorded black interstitial is visible. It is not a two-player run.
local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local home=assert(os.getenv('BAD_DUDES_HOME'))..'/'
local limit=tonumber(assert(os.getenv('BAD_DUDES_FRAMES')))
local n=0
local log=assert(io.open(out..'state.csv','w'))
local function save(path,data)
 local f=assert(io.open(path,'wb'));f:write(data);f:close()
end
local function frame()
 n=n+1
 log:write(n..','..emu.read(0x2c0,emu.memType.nesInternalRam)..','..emu.read(0x23f,emu.memType.nesInternalRam)..'\n')
 local diagnostic=os.getenv('MENU_GLYPH_DIAGNOSTIC')
 if diagnostic and n>=1710 and n<1750 then
  local digit=math.floor((n-1710)/4)
  for base=0x2000,0x2c00,0x400 do
   emu.write(base+14*32+19,0x02,emu.memType.nesPpuMemory)
   emu.write(base+16*32+16,digit==0 and 0x0a or digit,emu.memType.nesPpuMemory)
  end
 end
 if n%30==0 or (n>=1690 and n<=1780 and n%2==0) or (diagnostic and n>=1710 and n<=1752) then
  save(out..string.format('%06d.png',n),emu.takeScreenshot())
 end
 if n%1000==0 then log:flush();save(home..'progress',tostring(n)) end
 if n>=limit then log:close();save(home..'done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
