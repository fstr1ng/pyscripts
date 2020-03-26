import numpy      as np
import gnuplotlib as gp

x = np.arange(101) - 50
gp.plot(x**2)
#[ basic parabola plot pops up ]


g1 = gp.gnuplotlib(title = 'Parabola with error bars',
                   _with = 'xyerrorbars')
g1.plot( x**2 * 10, np.abs(x)/10, np.abs(x)*5,
         legend    = 'Parabola',
         tuplesize = 4 )
#[ parabola with x,y errobars pops up in a new window ]


x,y = np.ogrid[-10:11,-10:11]
gp.plot( x**2 + y**2,
         title     = 'Heat map',
         unset     = 'grid',
         cmds      = 'set view map',
         _with     = 'image',
         tuplesize = 3)
#[ Heat map pops up where first parabola used to be ]


theta = np.linspace(0, 6*np.pi, 200)
z     = np.linspace(0, 5,       200)
g2 = gp.gnuplotlib(_3d = True)
g2.plot( np.cos(theta),
         np.vstack((np.sin(theta), -np.sin(theta))),
         z )
#[ Two 3D spirals together in a new window ]


x = np.arange(1000)
gp.plot( (x*x, dict(histogram=1,            binwidth=10000)),
         (x*x, dict(histogram='cumulative', y2=1)))
#[ A density and cumulative histogram of x^2 are plotted together ]
