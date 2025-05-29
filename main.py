import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Circle

SUN_MASS = 1.477  
SUN_RADIUS = 696340 
BLACK_HOLE_MASS = 4.1e6 * SUN_MASS
BH_SCHWARZSCHILD = 2 * BLACK_HOLE_MASS 

fig = plt.figure(figsize=(16, 8))
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)  
ax2 = plt.subplot2grid((2, 2), (1, 0)) 
ax3 = plt.subplot2grid((2, 2), (1, 1))  
plt.subplots_adjust(bottom=0.3, hspace=0.4)

ax_sun_slider = plt.axes([0.25, 0.2, 0.6, 0.03])
ax_bh_slider = plt.axes([0.25, 0.15, 0.6, 0.03])

sun_slider = Slider(ax_sun_slider, 'Sun Distance (Solar radii)', 
                   0.5, 5.0, valinit=1.0) 
bh_slider = Slider(ax_bh_slider, 'Sgr A* Distance (Schwarzschild radii)', 
                  1.001, 10.0, valinit=5.0)

def time_dilation(r, schwarzschild_radius):
    with np.errstate(divide='ignore', invalid='ignore'):
        dilation = np.sqrt(1 - schwarzschild_radius/r)
        return np.where(r <= schwarzschild_radius, 0, dilation)

sun = Circle((2, 0), 0.3, color='orange', alpha=0.8)
bh = Circle((-2, 0), 0.5, color='black')
sun_observer = Circle((2.3, 0), 0.05, color='blue')
bh_observer = Circle((-2 + 5*0.5, 0), 0.05, color='red')

ax1.add_patch(sun)
ax1.add_patch(bh)
ax1.add_patch(sun_observer)
ax1.add_patch(bh_observer)
ax1.set_xlim(-5, 5)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Time Dilation Comparison: Sun vs. Sagittarius A*', pad=20)

sun_text = ax1.text(2, 1.5, "", ha="center", fontsize=10)
bh_text = ax1.text(-2, 1.5, "", ha="center", fontsize=10)
bh_warning = ax1.text(-2, 0, "", color="black", ha="center", va="center", 
                     fontsize=10, bbox=dict(facecolor="red", alpha=0.7))
sun_warning = ax1.text(2, 0, '', color="black", ha="center", va='center',
                      fontsize=10, bbox=dict(facecolor='yellow', alpha=0.7))

sun_radii = np.linspace(0.5, 5, 100) * SUN_RADIUS
sun_dilations = np.where(sun_radii < SUN_RADIUS, 
                        time_dilation(SUN_RADIUS, 2*SUN_MASS), 
                        time_dilation(sun_radii, 2*SUN_MASS))
bh_radii = np.linspace(1.001, 10, 100) * BH_SCHWARZSCHILD
bh_dilations = time_dilation(bh_radii, BH_SCHWARZSCHILD)

sun_line, = ax2.plot(sun_radii/SUN_RADIUS, sun_dilations, 'b-')
bh_line, = ax3.plot(bh_radii/BH_SCHWARZSCHILD, bh_dilations, 'r-')
ax2.axvline(x=1, color='orange', linestyle='--')
ax3.axvline(x=1, color='black', linestyle='--')

sun_marker = ax2.plot([1], [time_dilation(SUN_RADIUS, 2*SUN_MASS)], 'bo', markersize=8)
bh_marker = ax3.plot([5], [time_dilation(5*BH_SCHWARZSCHILD, BH_SCHWARZSCHILD)], 'ro', markersize=8)

for ax, title in zip([ax2, ax3], ['Sun Time Dilation', 'Sagittarius A* Time Dilation']):
    ax.set_xlabel('Distance (Object radii)')
    ax.set_ylabel('Time flow rate (t/t∞)')
    ax.grid(True)
    ax.set_title(title)
ax2.set_ylim(0.99998, 1.00002)
ax3.set_ylim(0, 1.1)

def update(val):
    sun_distance = max(0.1, sun_slider.val) * SUN_RADIUS  
    bh_distance = bh_slider.val * BH_SCHWARZSCHILD
    
    if sun_slider.val < 1.0: 
        sun_dilation = time_dilation(SUN_RADIUS, 2*SUN_MASS)
        sun_pos = sun_slider.val * 0.3
    else: 
        sun_dilation = time_dilation(sun_distance, 2*SUN_MASS)
        sun_pos = 0.3 + (sun_slider.val-1)*0.15  
        
    bh_dilation = time_dilation(bh_distance, BH_SCHWARZSCHILD)
    
    sun_observer.center = (2 + sun_pos, 0)
    bh_observer.center = (-2 + bh_slider.val*0.5, 0)
    
    sun_marker.set_data([sun_slider.val], [sun_dilation])
    bh_marker.set_data([bh_slider.val], [bh_dilation])
    
    if sun_slider.val < 1.0:
        sun_text.set_text(f'Inside Sun:\n{sun_dilation*100:.6f}%')
    else:
        sun_text.set_text(f'Sun at {sun_slider.val:.2f} Solar Radius:\n{sun_dilation*100:.6f}%')
    
    bh_text.set_text(f'Sgr A* at {bh_slider.val:.3f} Sch Radius:\n{bh_dilation*100:.2f}%')
    
    if bh_slider.val <= 1.1:
        bh_warning.set_text('EVENT HORIZON\nTIME FROZEN')
    else:
        bh_warning.set_text('')

    if 0.99 <= sun_slider.val <= 1.01:
        sun_warning.set_text('SUN SURFACE')
    else:
        sun_warning.set_text('')
    
    fig.canvas.draw_idle()

sun_slider.on_changed(update)
bh_slider.on_changed(update)

update(None)

plt.show()