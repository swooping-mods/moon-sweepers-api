#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "moon_sweepers/interaction_registry.h"
static MoonInteractionRegistry interactions;
static MoonInputRegistry input;
static unsigned char keys[256];
static unsigned polls[256];
static int query_flip;
static int poll(unsigned k){polls[k]++;return keys[k];}
typedef struct{int eligible;MoonInteractionTarget target;unsigned calls;} Target;
static int query(void *context,void *walker,MoonInteractionTarget *target){Target *t=context;assert(walker==(void *)1);t->calls++;*target=t->target;assert(!mir_sample(&interactions,1).selected);if(query_flip){keys['E']=1;query_flip=0;}return t->eligible;}
static unsigned add(const char *name,const char *binding,unsigned flags,Target *target,unsigned owner){MoonInteractionActionV1 spec={sizeof(spec),flags,name,binding,query,target};return mir_register(&interactions,&input,&spec,owner);}
static void begin(unsigned long long frame){mir_begin(&interactions,&input,frame,(void *)1);}
static MoonInputState peer(unsigned action){unsigned k=input.actions[action-1].chord.key;int admit=!mir_blocked(&interactions,action,k);MoonInputState s=mi_sample(&input,action,admit);return admit?s:(MoonInputState){0};}
int main(void){
 input.key=poll;Target plush={1,{11,2,0,1},0},bed={1,{12,3,0,2},0},slime={1,{13,2.3f,0,3},0};
 unsigned p=add("squishy-plushie.pickup-release","E",MOON_INTERACTION_EXCLUSIVE,&plush,1),b=add("native-bed.use","E",0,&bed,2),s=add("slime-pet.interact","E",MOON_INTERACTION_EXCLUSIVE,&slime,3);assert(p&&b&&s);
 unsigned map=mi_register(&input,"portable-map.toggle","E"),walk=mi_register(&input,"player.walk","W");
 begin(0);assert(mir_sample(&interactions,p).selected);assert(!mir_sample(&interactions,p).input.pressed);begin(0);assert(plush.calls==1);
 keys['E']=keys['W']=1;begin(1);assert(mir_sample(&interactions,p).input.pressed);assert(!mir_sample(&interactions,b).input.held&&!mir_sample(&interactions,s).input.pressed);assert(!peer(map).pressed&&peer(walk).pressed);assert(mir_blocked(&interactions,0,'E')&&!mir_blocked(&interactions,0,'W'));
 plush.eligible=0;slime.target.priority=100;begin(2);assert(!mir_sample(&interactions,s).input.pressed&&!peer(map).held); /* Latch survives lost target. */
 keys['E']=0;begin(3);assert(mir_blocked(&interactions,0,'E')&&!peer(map).released);begin(4);assert(!mir_blocked(&interactions,0,'E'));
 keys['E']=1;begin(5);assert(mir_sample(&interactions,s).input.pressed&&!peer(map).pressed); /* Carried pet beats nearer bed. */
 keys['E']=0;begin(6);(void)peer(map);begin(7);(void)peer(map);slime.eligible=0;bed.target.distance=1;keys['E']=1;begin(8);assert(mir_sample(&interactions,b).input.pressed&&peer(map).pressed);assert(!mir_blocked(&interactions,0,'E')); /* Explicit nonexclusive behavior. */
 keys['E']=0;begin(9);plush.eligible=1;bed.eligible=0;plush.target.distance=0.5f;
 assert(mi_rebind(&input,interactions.entries[p-1].action,"Ctrl+Q"));assert(mi_rebind(&input,map,"Ctrl+Q"));keys['Q']=1;begin(10);assert(!mir_sample(&interactions,p).input.pressed&&!peer(map).pressed);
 keys[17]=1;begin(11);assert(mir_sample(&interactions,p).input.pressed&&!peer(map).held);assert(mir_blocked(&interactions,0,'Q')&&!mir_blocked(&interactions,0,'E'));
 keys['Q']=0;begin(12);begin(13);keys[17]=0;
 /* A gate opening while held consumes edges, and an invalid target is never a
  * reason to suppress vanilla. Check both NaN and an unbounded distance. */
 assert(mi_rebind(&input,interactions.entries[p-1].action,"E"));plush.eligible=0;keys['E']=1;begin(14);plush.eligible=1;begin(15);assert(mir_sample(&interactions,p).input.held&&!mir_sample(&interactions,p).input.pressed&&!mir_blocked(&interactions,0,'E'));
 keys['E']=0;begin(16);plush.target.distance=0.0f/0.0f;keys['E']=1;begin(17);assert(!mir_sample(&interactions,p).selected&&!mir_blocked(&interactions,0,'E'));plush.target.distance=101;begin(18);assert(!mir_sample(&interactions,p).selected);
 plush.target.distance=1;keys['E']=0;begin(19);keys['E']=1;mir_begin(&interactions,&input,20,0);assert(!mir_sample(&interactions,p).selected&&!mir_blocked(&interactions,0,'E'));begin(21);assert(!mir_sample(&interactions,p).input.pressed);
 /* Equal distances settle by stable action name even in reverse registration
  * order. Different physical keys remain independent. */
 memset(&interactions,0,sizeof(interactions));memset(&input,0,sizeof(input));memset(keys,0,sizeof(keys));input.key=poll;
 Target a={1,{1,1,0,1},0},z={1,{2,1,0,2},0};unsigned iz=add("z-target.use","E",1,&z,1),ia=add("a-target.use","E",1,&a,2),mouse=add("plush.throw","LeftMouse",1,&a,3);begin(1);keys['E']=keys[1]=1;begin(2);assert(mir_sample(&interactions,ia).input.pressed&&!mir_sample(&interactions,iz).selected&&mir_sample(&interactions,mouse).input.pressed);
 assert(!add("a-target.use","E",1,&a,2));assert(!add("bad","E",1,&a,2));assert(!add("bad.flags","E",2,&a,2));assert(!add("bad.owner","E",1,&a,0));
 mir_rollback(&interactions,3);assert(interactions.count==2); /* Failed ModStart cannot leave a query. */
 memset(&interactions,0,sizeof(interactions));memset(&input,0,sizeof(input));memset(keys,0,sizeof(keys));input.key=poll;
 z.target.distance=2;a.target.distance=1;unsigned generic=add("modifier.generic","Ctrl",1,&z,1),left=add("modifier.left","LeftCtrl",1,&a,2),right=add("modifier.right","RightCtrl",1,&z,3);assert(generic&&left&&right);
 unsigned generic_peer=mi_register(&input,"map.ctrl","Ctrl");keys[17]=keys[162]=1;begin(1);
 assert(mir_take(&interactions,left)&&!mir_take(&interactions,generic)&&!mir_take(&interactions,right));assert(mir_blocked(&interactions,0,17)&&mir_blocked(&interactions,0,162)&&!mir_blocked(&interactions,0,163));assert(!peer(generic_peer).held);
 memset(keys,0,sizeof(keys));begin(2);begin(3);a.eligible=0;keys[17]=keys[163]=1;begin(4);
 assert(mir_take(&interactions,generic)&&!mir_take(&interactions,right));assert(interactions.captured[163]&&!interactions.captured[162]);
 memset(keys,0,sizeof(keys));begin(5);begin(6);a.eligible=1;
 /* Disable only the generic offer without changing the shared target data. */
 Target unavailable={0,{3,1,0,0},0};interactions.entries[generic-1].context=&unavailable;
 keys[17]=keys[162]=keys[163]=1;begin(7);assert(mir_take(&interactions,left)&&mir_take(&interactions,right));
 memset(&interactions,0,sizeof(interactions));memset(&input,0,sizeof(input));memset(keys,0,sizeof(keys));input.key=poll;
 unsigned snapshot=add("snapshot.use","E",1,&a,1);query_flip=1;begin(1);assert(!mir_sample(&interactions,snapshot).input.pressed&&!interactions.captured['E']);begin(2);assert(mir_take(&interactions,snapshot));begin(3);assert(interactions.captured['E']);
 for(unsigned n=interactions.count;n<MOON_INTERACTION_CAPACITY;n++){char name[64];snprintf(name,sizeof(name),"capacity.action-%u",n);assert(add(name,"None",0,&a,4));}assert(!add("capacity.overflow","E",0,&a,4));
 /* Only registered bindings/modifiers and live captures need physical polls.
  * A supplied snapshot may alias the registry's previous down array. */
 memset(&interactions,0,sizeof(interactions));memset(&input,0,sizeof(input));memset(keys,0,sizeof(keys));memset(polls,0,sizeof(polls));input.key=poll;
 unsigned bounded=add("bounded.use","E",1,&a,1);assert(bounded);assert(mi_register(&input,"unrelated.walk","W"));begin(100);
 assert(polls['E']==1&&polls['W']==1&&polls[16]==1&&polls[17]==1&&polls[18]==1&&!polls['Z']);
 keys['E']=1;begin(101);assert(mir_take(&interactions,bounded));
 assert(mi_rebind(&input,interactions.entries[bounded-1].action,"Q"));begin(102);assert(mir_blocked(&interactions,0,'E'));
 input.snapshot=interactions.down;interactions.down['E']=0;begin(103);assert(mir_blocked(&interactions,0,'E'));
 begin(104);assert(!mir_blocked(&interactions,0,'E')&&input.snapshot==interactions.down);input.snapshot=0;
 puts("interaction arbitration: overlap, native-mask contract, remap, release, gates, ordering, rollback and capacity passed");return 0;
}
