#include <stdatomic.h>
#include <stdint.h>
#include <string.h>
typedef struct { unsigned abi,size; int (*add)(int,int); } Math;
typedef struct { unsigned size,abi; void *publish; const void *(*find)(const char *,const char *,unsigned,unsigned); void *subscribe,*unsubscribe; } Runtime;
static _Atomic unsigned state,lookups;
static unsigned mode;
static int add(int a,int b){return a+b;}
static int stub(void){return 0;}
static const Math math={7,sizeof(Math),add};
static const void *find(const char *owner,const char *service,unsigned abi,unsigned size){
    atomic_fetch_add(&lookups,1);
    return !strcmp(owner,"3d-tools")&&!strcmp(service,"math--plus-")&&abi==7&&size<=sizeof(math)?&math:0;
}
static Runtime runtime;
void fixture_mode(unsigned value){
    mode=value;runtime=(Runtime){sizeof(Runtime),1,(void *)stub,find,(void *)stub,(void *)stub};
    if(value==3)runtime.size=32;
    if(value==4)runtime.abi=2;
    if(value==5)runtime.publish=0;
    atomic_store(&state,0);atomic_store(&lookups,0);
}
void fixture_state(unsigned value){atomic_store(&state,value);}
unsigned fixture_lookups(void){return atomic_load(&lookups);}
unsigned MoonLab_LoaderAbi(void){return mode==1?2:1;}
unsigned MoonLab_RuntimeState_v1(void){return atomic_load(&state);}
const Runtime *MoonLab_GetRuntimeApi_v1(void){return mode==2?0:&runtime;}
