#include <stdio.h>

typedef struct {
  float x, y, z;
} vec3;

int main(void) {
  vec3 pos = {0};
  pos.x = 0;
  pos.y = 0;
  pos.z = 0;
  printf("hello\n");
  return 0;
}
