/* Production session helper: read-only capture can fail while release is denied.
 * The caller must retain the partial session and explicitly finish it later. */
#include <assert.h>
#include <stdio.h>
#include "moon_sweepers/camera.h"
static int world,walker,camera,roots,claims,releases,captures,restores;
static int release_ok,restore_ok=1,lease;
static MoonCameraSession session;
static const MoonCameraApiV1 api;
static unsigned claim(const char *owner,void *w,void *p,void *c,unsigned resources){
  assert(owner&&w==&world&&p==&walker&&c==&camera&&resources==MOON_CAMERA_MODE);
  assert(!lease);claims++;lease=1;return 37;
}
static int held(const char *owner,unsigned token){assert(owner&&token==37);return lease;}
static int release(const char *owner,unsigned token){
  assert(owner&&token==37&&lease);releases++;
  if(!release_ok)return 0;
  lease=0;return 1;
}
static const MoonCameraApiV1 api={sizeof(api),MOON_CAMERA_ABI,claim,held,release};
static int capture_failure(void *context){
  assert(context==&roots&&session.api==&api&&session.token==37);
  roots=2;captures++;return 0;
}
static int finish_partial(void *context){
  assert(context==&roots&&lease&&session.token==37&&roots==2);
  restores++;return restore_ok;
}
int main(void){
  assert(!moon_camera_begin(&session,&api,"view",&world,&walker,&camera,
                            MOON_CAMERA_MODE,capture_failure,&roots));
  assert(session.token==37&&session.api==&api&&session.owner&&lease);
  assert(roots==2&&claims==1&&captures==1&&releases==1);
  /* Reentry must not claim a second lease or overwrite the cleanup context. */
  assert(!moon_camera_begin(&session,&api,"replacement",&world,&walker,&camera,
                            MOON_CAMERA_MODE,capture_failure,&roots));
  assert(claims==1&&captures==1&&roots==2);
  restore_ok=0;
  assert(!moon_camera_finish(&session,finish_partial,&roots));
  assert(roots==2&&session.token==37&&releases==1);
  restore_ok=1;
  assert(!moon_camera_finish(&session,finish_partial,&roots));
  assert(roots==2&&session.token==37&&releases==2&&lease);
  release_ok=1;
  assert(moon_camera_finish(&session,finish_partial,&roots));
  assert(!session.token&&!session.api&&!session.owner&&!lease&&restores==3);
  roots=0; /* Provider drops partial roots only after cleanup acknowledges. */
  assert(moon_camera_finish(&session,finish_partial,&roots));
  assert(releases==3&&restores==3);
  /* Acknowledged release on the original failed begin clears every field. */
  assert(!moon_camera_begin(&session,&api,"view",&world,&walker,&camera,
                            MOON_CAMERA_MODE,capture_failure,&roots));
  assert(!session.token&&!session.api&&!session.owner&&!lease&&claims==2);
  roots=0;
  puts("camera failed capture, retained release token and explicit cleanup retry passed");
  return 0;
}
