n=1;
max=10;
while [ "$n" -le "$max" ]; do
  mkdir "w$n"
  n=`expr "$n" + 1`;
done