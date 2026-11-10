/* Public connector behavior against owned fake platform and domain functions. */
#include <stdio.h>
#include <string.h>
#define __declspec(x)
#define __stdcall
typedef void *PTR;
typedef unsigned int DWORD;
#include "moon_sweepers/services.h"
#include "moon_sweepers/build_menu/build_menu.h"
static unsigned loader_kind,runtime_present,loads,starts,lookups,frames;
static MoonBuildMenu building={MB_ABI,sizeof(MoonBuildMenu),0,0};
static int publish(const MoonServicePublicationV1 *p){(void)p;return 1;}
static const void *find(const char *owner,const char *name,unsigned abi,unsigned size){
    lookups++;
    return !strcmp(owner,"build-menu-framework")&&!strcmp(name,"build-menu")
        &&abi==MB_ABI&&size==sizeof(building)?&building:0;
}
static unsigned subscribe(const MoonFrameSubscriptionV1 *spec){
    frames++;
    return spec->size==sizeof(*spec)&&spec->phase==MOON_PHASE_NORMAL&&spec->callback?7:0;
}
static int unsubscribe(unsigned handle){return handle==7;}
static MoonRuntimeApiV1 runtime={sizeof(runtime),MOON_RUNTIME_SERVICES_ABI,publish,find,subscribe,unsubscribe};
static const MoonRuntimeApiV1 *get_runtime(void){return &runtime;}
static int start(PTR domain,PTR game){(void)domain;(void)game;starts++;return 1;}
static const MoonBuildMenu *get_building(unsigned abi,unsigned size){return abi==MB_ABI&&size==sizeof(building)?&building:0;}
static PTR GetModuleHandleA(const char *name){return loader_kind&&!strcmp(name,"version.dll")?(PTR)1:0;}
static PTR GetProcAddress(PTR module,const char *name){
    if(module==(PTR)1){
        if(!strcmp(name,"MoonLab_LoaderAbi"))return loader_kind==2?(PTR)1:0;
        if(!strcmp(name,"MoonLab_GetRuntimeApi_v1"))return runtime_present?(PTR)get_runtime:0;
    }
    if(module==(PTR)2){
        if(!strcmp(name,"MoonLab_ModStart"))return (PTR)start;
        if(!strcmp(name,"MoonLab_BuildMenu_v1"))return (PTR)get_building;
    }
    return 0;
}
static PTR LoadLibraryA(const char *path){
    loads++;
    return !strcmp(path,"C:\\Game\\MoonLab\\mods\\build-menu-framework\\mod.dll")?(PTR)2:0;
}
DWORD GetModuleFileNameA(PTR module,char *out,DWORD size){
    (void)module;const char *path="C:\\Game\\MoonSweepers.exe";
    if(strlen(path)>=size)return 0;
    strcpy(out,path);return (DWORD)strlen(path);
}
static void cat(char *out,const char *text){strcpy(out,text);}
#include "moon_sweepers/build_menu/client.h"
#define CHECK(x) do{if(!(x)){fprintf(stderr,"line %d: %s\n",__LINE__,#x);return 1;}}while(0)
static void frame(void *walker,void *user){(void)walker;(void)user;}
int main(void){
    CHECK(MoonLab_RuntimeServicesAbi()==1);
    /* No recognized loader keeps the existing standalone modkit behavior. */
    CHECK(mb_connect(0,0)==&building&&loads==1&&starts==1);
    loader_kind=1;CHECK(mb_connect(0,0)==&building&&loads==2&&starts==2);
    loads=starts=0;loader_kind=2;
    CHECK(!mb_connect(0,0)&&!loads&&!starts&&!lookups);
    runtime_present=1;runtime.abi=2;CHECK(!mb_connect(0,0));runtime.abi=1;
    runtime.size--;CHECK(!mb_connect(0,0));runtime.size++;
    runtime.find=0;CHECK(!mb_connect(0,0));runtime.find=find;
    CHECK(!loads&&!starts&&!lookups);
    building.abi=2;CHECK(!mb_connect(0,0));building.abi=MB_ABI;
    building.size--;CHECK(!mb_connect(0,0));building.size++;
    CHECK(mb_connect(0,0)==&building&&lookups==3&&!loads&&!starts);
    CHECK(moon_runtime_subscribe_frame(frame,0)==7&&frames==1);
    CHECK(!loads&&!starts);
    puts("public client uses committed runtime tables without private startup");return 0;
}
