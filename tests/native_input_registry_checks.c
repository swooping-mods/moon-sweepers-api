#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "moon_sweepers/input_registry.h"
static unsigned char keys[256];
static int poll(unsigned key){return keys[key];}
static int resolve(const char *name,char *text,unsigned size){if(strcmp(name,"gambling.wager"))return 0;return snprintf(text,size,"Alt+F8")>0;}
static int malformed(const char *name,char *text,unsigned size){(void)name;return snprintf(text,size,"bad-key")>0;}
static MoonInputRegistry registry;
static void clear_keys(void){memset(keys,0,sizeof(keys));}
int main(void){
    registry.key=poll;MoonInputChord chord;
    assert(mi_parse("!Shift+!Alt+Ctrl+K",&chord));assert(chord.key=='K'&&chord.required==1&&chord.forbidden==6);
    assert(mi_parse("None",&chord)&&!chord.key);assert(mi_parse("F24",&chord)&&chord.key==135);
    assert(mi_parse("VK255",&chord)&&chord.key==255);assert(!mi_parse("VK256",&chord));
    assert(!mi_parse("Ctrl+!Ctrl+K",&chord));assert(!mi_parse("Ctrl+",&chord));assert(!mi_parse("A+B",&chord));assert(!mi_parse("!Shift",&chord));
    assert(!mi_parse("F0",&chord));assert(!mi_parse("F25",&chord));assert(!mi_parse("Ctrl+Super+K",&chord));assert(!mi_parse("Ctrl+None",&chord));
    assert(!mi_register(&registry,"unqualified","K"));assert(!mi_register(&registry,"bad name.action","K"));
    keys['J']=1;unsigned first_edge=mi_register(&registry,"first.edge","J");assert(mi_sample(&registry,first_edge,1).pressed);clear_keys();
    mi_configure(&registry,malformed);unsigned invalid_override=mi_register(&registry,"invalid.override","E");MoonInputActionInfo first={.size=sizeof(first)};assert(mi_describe(&registry,invalid_override-1,&first)&&!strcmp(first.binding,"E"));mi_configure(&registry,0);
    unsigned stack=mi_register(&registry,"item-stacking.stack","!Shift+!Alt+Ctrl+K");assert(stack);
    assert(mi_register(&registry,"item-stacking.stack","J")==stack);
    MoonInputState state=mi_sample(&registry,stack,1);assert(!state.held&&!state.pressed&&!state.released);
    keys[17]=keys['K']=1;state=mi_sample(&registry,stack,1);assert(state.held&&state.pressed);
    state=mi_sample(&registry,stack,1);assert(state.held&&!state.pressed);
    state=mi_sample(&registry,stack,0);assert(!state.held&&!state.pressed&&state.released);
    state=mi_sample(&registry,stack,1);assert(state.held&&!state.pressed); /* Focus return consumes the held edge. */
    clear_keys();assert(mi_sample(&registry,stack,1).released);
    keys[17]=keys[16]=keys['K']=1;assert(!mi_sample(&registry,stack,1).pressed);
    keys[16]=0;assert(!mi_sample(&registry,stack,1).pressed); /* Wider terminal chord cannot become stacking. */
    keys['K']=0;mi_sample(&registry,stack,1);keys['K']=1;assert(mi_sample(&registry,stack,1).pressed);
    assert(mi_rebind(&registry,stack,"K"));assert(!mi_sample(&registry,stack,1).held); /* Held rebind waits for release. */
    keys['K']=0;mi_sample(&registry,stack,1);keys['K']=1;assert(mi_sample(&registry,stack,1).pressed);
    assert(!mi_rebind(&registry,stack,"bad-key"));MoonInputActionInfo info={.size=sizeof(info)};assert(mi_describe(&registry,stack-1,&info));assert(!strcmp(info.binding,"K"));
    assert(mi_rebind(&registry,stack,"None"));assert(!mi_sample(&registry,stack,1).held);
    clear_keys();unsigned wager=mi_register(&registry,"gambling.wager","Ctrl+G");mi_configure(&registry,resolve);
    assert(mi_describe(&registry,wager-1,&info)&&!strcmp(info.binding,"Alt+F8"));
    unsigned later=mi_register(&registry,"custom-keybinds.reload","Ctrl+Home");assert(mi_describe(&registry,later-1,&info)&&!strcmp(info.binding,"Ctrl+Home"));
    keys[18]=keys[119]=1;assert(mi_sample(&registry,wager,1).pressed);
    mi_configure(&registry,0);assert(mi_describe(&registry,wager-1,&info)&&!strcmp(info.binding,"Ctrl+G"));
    clear_keys();keys[17]=keys['G']=1;assert(mi_sample(&registry,wager,1).pressed);
    /* Claims arbitrate only explicit channels; unrelated actions still work. */
    assert(mi_claim(&registry,"world-interact",0,"slime-pet"));assert(mi_claim(&registry,"world-interact",0,"slime-pet"));assert(!mi_claim(&registry,"world-interact",0,"little-helpers"));
    assert(mi_claim(&registry,"world-interact",1,"little-helpers"));assert(mi_claim(&registry,"camera",1,"building-drone"));
    assert(!mi_claim(&registry,"",1,"bad"));assert(!mi_claim(&registry,"world-interact",1,""));
    for(unsigned i=registry.count;i<MOON_INPUT_ACTION_CAPACITY;i++){char name[64];snprintf(name,sizeof(name),"capacity.action-%u",i);assert(mi_register(&registry,name,"E"));}
    assert(!mi_register(&registry,"capacity.overflow","E"));assert(!mi_sample(&registry,0,1).pressed);assert(!mi_rebind(&registry,0,"E"));assert(!mi_describe(&registry,registry.count,&info));
    for(unsigned i=2;i<MOON_INPUT_CLAIM_CAPACITY;i++){char channel[32];snprintf(channel,sizeof(channel),"channel-%u",i);assert(mi_claim(&registry,channel,1,"owner"));}
    assert(!mi_claim(&registry,"overflow",1,"owner"));
    puts("shared input registry production checks passed");return 0;
}
