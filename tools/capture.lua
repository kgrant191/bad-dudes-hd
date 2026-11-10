local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local function mem(t,size)
 local a={};for i=0,size-1 do a[#a+1]=string.char(emu.read(i,t)) end;return table.concat(a)
end
local function frame()
 n=n+1
 if n%120==0 or n==1 then
  save(out..string.format('%05d.png',n),emu.takeScreenshot())
  local s=emu.getState();local lines={};for k,v in pairs(s) do lines[#lines+1]=k..'='..tostring(v) end;table.sort(lines);save(out..string.format('%05d.txt',n),table.concat(lines,'\n'))
  save(out..string.format('%05d.ppu',n),mem(emu.memType.nesPpuMemory,0x4000))
  save(out..string.format('%05d.oam',n),mem(emu.memType.nesSpriteRam,256))
  save(out..string.format('%05d.ram',n),mem(emu.memType.nesInternalRam,2048))
  local maps={};for a=0,0x1fff,16 do local m=emu.convertAddress(a,emu.memType.nesPpuMemory);maps[#maps+1]=a..','..m.address..','..m.memType end;save(out..string.format('%05d.map',n),table.concat(maps,'\n'))
 end
 if n>=8500 then save(assert(os.getenv('BAD_DUDES_HOME'))..'/done','done');emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
