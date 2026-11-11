#include "pch.h"
#include "Shared/Emulator.h"
#include "Shared/EmuSettings.h"
#define private public
#include "NES/NesConsole.h"
#undef private
#include "NES/HdPacks/HdPackBuilder.h"
#include <filesystem>
#include <set>
#include "NES/HdPacks/HdNesPpu.h"
#include "Shared/NotificationManager.h"
extern std::unique_ptr<Emulator> _emu;
extern "C" {
void InitDll();
void InitializeEmu(const char*,void*,void*,bool,bool,bool,bool);
bool LoadRom(const char*,const char*);
void Pause(); void Resume(); void Stop(); void Release();
void MoviePlay(const char*);
int LoadScript(const char*,const char*,const char*,int);
void GetScriptLog(int,char*,uint32_t);
void GetLog(char*,uint32_t);
}
class CaptureListener : public INotificationListener {
public:
 int count=0;
 void ProcessNotification(ConsoleNotificationType type, void* param) override {
 if(type!=ConsoleNotificationType::PpuFrameDone) return;
 count++;
 if(count%120!=0 && !(count>=380 && count<=800 && count%6==0)) return;
 auto nes=std::dynamic_pointer_cast<NesConsole>(_emu->GetConsole());
 auto ppu=dynamic_cast<HdNesPpu*>(nes->GetPpu()); if(!ppu)return;
 auto info=ppu->_info==ppu->_screenInfo[0]?ppu->_screenInfo[1]:ppu->_screenInfo[0];
 std::set<std::tuple<int,int,int,int,uint32_t,int,int>> entries;
 for(int y=0;y<240;y++) for(int x=0;x<256;x++){
 auto &px=info->ScreenTiles[y*256+x];
 auto add=[&](HdPpuTileInfo&t,int layer){if(t.TileIndex<0)return;int oy=t.OffsetY; if(layer && t.VerticalMirroring)oy=7-oy;entries.insert({layer,x-t.OffsetX,y-oy,t.TileIndex,t.PaletteColors,t.HorizontalMirroring,t.VerticalMirroring});};
 add(px.Tile,0);for(int k=0;k<px.SpriteCount;k++)add(px.Sprite[k],1);
 }
 const char* dir=std::getenv("BAD_DUDES_METADATA_DIR"); if(!dir)return; char leaf[64];snprintf(leaf,sizeof(leaf),"%05d.tiles",count);std::ofstream out(std::filesystem::path(dir)/leaf);
 for(auto &e:entries){auto [l,x,y,t,p,h,v]=e;out<<l<<","<<x<<","<<y<<","<<t<<","<<p<<","<<h<<","<<v<<"\n";}
 }
};
int main(int argc,char**argv){
 if(argc<6) return 2;
 InitDll();
 InitializeEmu(argv[1],nullptr,nullptr,true,true,true,true);
 auto settings=_emu->GetSettings();
 auto &n=settings->GetNesConfig();
 n.Port1.Type=ControllerType::NesController;n.Port2.Type=ControllerType::NesController;
 n.EnableHdPacks=true;
 const uint32_t pal[64]={
 #include "palette.inc"
 };
 for(int i=0;i<512;i++) n.UserPalette[i]=pal[i%64];
 settings->GetDebugConfig().ScriptAllowIoOsAccess=true;
 settings->SetFlag(EmulationFlags::ConsoleMode);
 settings->SetFlag(EmulationFlags::MaximumSpeed);
 Pause();
 if(!LoadRom(argv[2],"")) return 3;
 MoviePlay(argv[3]);
 auto nes=std::dynamic_pointer_cast<NesConsole>(_emu->GetConsole());
 bool build=std::string(argv[5])!="-";
 if(build){
 HdPackBuilderOptions opts={};opts.SaveFolder=argv[5];opts.FilterType=ScaleFilterType::Prescale;opts.Scale=1;opts.ChrRamBankSize=0x1000;opts.IgnoreOverscan=true;
 nes->StartRecordingHdPack(opts);
 }
 std::ifstream f(argv[4]);std::string script((std::istreambuf_iterator<char>(f)),{});
 int id=LoadScript("capture",argv[1],script.c_str(),-1);
 auto listener=std::make_shared<CaptureListener>();
 if(!build && !std::getenv("SKIP_METADATA")) _emu->GetNotificationManager()->RegisterNotificationListener(listener);
 Resume();
 for(int i=0;i<6000;i++){
 std::this_thread::sleep_for(std::chrono::milliseconds(100));
 if(std::filesystem::exists(std::string(argv[1])+"/done")) break;
 if(i%100==0){char log[16384]={};GetScriptLog(id,log,sizeof(log));std::cerr<<log<<std::endl;}
 }
 Pause();if(build) nes->StopRecordingHdPack();
 char log[32768]={};GetLog(log,sizeof(log));std::cout<<log<<std::endl;
 GetScriptLog(id,log,sizeof(log));std::cout<<log<<std::endl;
 nes.reset();Stop();Release();return 0;
}
