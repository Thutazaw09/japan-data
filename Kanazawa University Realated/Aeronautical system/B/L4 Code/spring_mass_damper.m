function dxdt = spring_mass_damper(t,x)

x1 = x(1);
x2 = x(2);

m = 1;
c = 1;
k = -1;
F = 0;

x1dot = x2;
x2dot = -c/m*x2 - k/m*x1 - F/m;

dxdt = [x1dot
        x2dot];

