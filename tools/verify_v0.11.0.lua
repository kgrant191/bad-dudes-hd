local out=assert(os.getenv('BAD_DUDES_CAPTURE_DIR'))..'/'
local n=0
local previous=-1
local dense_until=0
local ramlog=assert(io.open(out..'palette.csv','w'))
local function save(path,data) local f=assert(io.open(path,'wb'));f:write(data);f:close() end
local log=assert(io.open(out..'state.csv','w'))
local function frame()
 n=n+1
 local scene=emu.read(0x2c0,emu.memType.nesInternalRam)
 local hero=emu.read(0x23f,emu.memType.nesInternalRam)
 log:write(n..','..scene..','..hero..'\n')
 local vals={n,scene,hero,emu.read(0x3e6,emu.memType.nesInternalRam)}
 for a=0x471,0x490 do vals[#vals+1]=emu.read(a,emu.memType.nesInternalRam) end
 ramlog:write(table.concat(vals,',')..'\n')
 if scene~=previous then dense_until=n+150;previous=scene end
 local transition=false
 for _,f in ipairs({1696,7012,15342,25236,36412,51146,64085,82098,82102,82779,89942,90003,90175}) do if n>=f-48 and n<=f+24 then transition=true end end
 local focused=(n>=22490 and n<=22630) or (n>=62990 and n<=63065) or (n>=80970 and n<=81130)
 if n%60==0 or focused or (transition and n%2==0) or (n<=dense_until and n%2==0) or os.getenv('CAPTURE_ALL_FRAMES') then save(out..string.format('%06d.png',n),emu.takeScreenshot()) end
 if n%1000==0 then log:flush();save(assert(os.getenv('BAD_DUDES_HOME'))..'/progress',tostring(n)) end
 if n>=tonumber(os.getenv('BAD_DUDES_FRAMES')) then ramlog:close();log:close();save(assert(os.getenv('BAD_DUDES_HOME'))..'/done',tostring(n));emu.breakExecution() end
end
emu.addEventCallback(frame,emu.eventType.endFrame)
