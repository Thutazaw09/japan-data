clear all

tspan = [0 15];
x10 = 1;
x20 = 0;

x0 = [x10
      x20];

[t,x] = ode45(@spring_mass_damper,tspan,x0);
plot(t,x)
xlabel('Time')
ylabel('x')
legend('x1','x2')


