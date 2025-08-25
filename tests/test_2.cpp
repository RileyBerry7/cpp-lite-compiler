int main(int argc, char param = 'x')
{
  int x = 1, y = {2}, z = x + y * 3;
  x += y, z -= 1;
  if (x < z)
    x++;
  else {
    y = x ? y : z;
  }
  while (x < 10)
    x = x * 2;
  do z--; while (z > 0);
  for (int i = 0; i < 5; i++)
    x = x + i;
  switch (x) {
    case 1: break;
    case 2: x = 3; break;
    default: x = 4;
  }
  label1: goto label1;
  return;
}
